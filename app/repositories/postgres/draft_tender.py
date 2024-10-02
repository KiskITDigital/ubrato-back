from datetime import datetime
from typing import Any, List

from config import get_config
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import RepositoryException
from repositories.postgres.schemas import (
    City,
    DraftTender,
    DraftTenderObjectType,
    DraftTenderServiceType,
    ObjectGroup,
    ObjectType,
    ServiceGroup,
    ServiceType,
)
from schemas import models
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class DraftTenderRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db
        self.localization = get_config().Localization.config

    async def create_tender(
        self,
        tender: DraftTender,
        service_type_ids: List[int],
        object_type_ids: List[int],
    ) -> DraftTender:
        self.db.add(tender)
        await self.db.flush()
        for id in service_type_ids:
            self.db.add(
                DraftTenderServiceType(
                    tender_id=tender.id,
                    service_type_id=id,
                )
            )

        for id in object_type_ids:
            self.db.add(
                DraftTenderObjectType(
                    tender_id=tender.id,
                    object_type_id=id,
                )
            )

        await self.db.commit()

        await self.db.refresh(tender)

        return tender

    async def update_draft_tender(
        self, tender: dict[str, Any], id: int
    ) -> DraftTender:
        query = await self.db.execute(
            select(DraftTender).where(DraftTender.id == id)
        )

        tender_to_update = query.scalar()

        if tender_to_update is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="",
                sql_msg="",
            )

        for key, value in tender.items():
            setattr(tender_to_update, key, value)

        tender_to_update.update_at = datetime.now()

        await self.db.execute(
            delete(DraftTenderServiceType).where(
                DraftTenderServiceType.tender_id == tender_to_update.id,
            )
        )

        await self.db.execute(
            delete(DraftTenderObjectType).where(
                DraftTenderObjectType.tender_id == tender_to_update.id,
            )
        )

        await self.db.flush()

        for id in tender["services_types"]:
            self.db.add(
                DraftTenderServiceType(
                    tender_id=tender_to_update.id,
                    service_type_id=id,
                )
            )

        for id in tender["objects_types"]:
            self.db.add(
                DraftTenderObjectType(
                    tender_id=tender_to_update.id,
                    object_type_id=id,
                )
            )

        await self.db.commit()
        await self.db.refresh(tender_to_update)
        return tender_to_update

    async def get_draft_tender_by_id(
        self, tender_id: int
    ) -> models.DraftTender:
        query = await self.db.execute(
            select(DraftTender).where(DraftTender.id == tender_id)
        )

        tender = query.scalar()

        if tender is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.localization["errors"]["no_draft_tender"],
                sql_msg="",
            )

        return await self.format_draft_tender(
            tender=tender,
        )

    async def delete_draft_tender(self, id: int) -> None:
        await self.db.execute(
            delete(DraftTenderServiceType).where(
                DraftTenderServiceType.tender_id == id,
            )
        )

        await self.db.execute(
            delete(DraftTenderObjectType).where(
                DraftTenderObjectType.tender_id == id,
            )
        )

        await self.db.execute(delete(DraftTender).where(DraftTender.id == id))

        await self.db.commit()

    async def format_draft_tender(
        self,
        tender: DraftTender,
    ) -> models.DraftTender:
        services_type_names: List[int] = []

        query = await self.db.execute(
            select(ServiceType.id)
            .join(
                DraftTenderServiceType,
                DraftTenderServiceType.service_type_id == ServiceType.id,
            )
            .where(DraftTenderServiceType.tender_id == tender.id)
        )

        for id in query.scalars():
            services_type_names.append(id)

        services_groups_names: dict[int, None] = {}

        query = await self.db.execute(
            select(ServiceGroup.id)
            .select_from(ServiceType)
            .join(
                ServiceGroup,
                ServiceType.service_group_id == ServiceGroup.id,
            )
            .where(
                and_(
                    DraftTenderServiceType.service_type_id == ServiceType.id,
                    DraftTenderServiceType.tender_id == tender.id,
                )
            )
        )

        for id in query.scalars():
            services_groups_names[id] = None

        objects_type_names: List[int] = []

        query = await self.db.execute(
            select(ObjectType.id)
            .join(
                DraftTenderObjectType,
                DraftTenderObjectType.object_type_id == ObjectType.id,
            )
            .where(DraftTenderObjectType.tender_id == tender.id)
        )

        for id in query.scalars():
            objects_type_names.append(id)

        query = await self.db.execute(
            select(ObjectGroup.id)
            .select_from(ObjectType)
            .join(
                ObjectGroup,
                ObjectType.object_group_id == ObjectGroup.id,
            )
            .where(
                and_(
                    DraftTenderObjectType.object_type_id == ObjectType.id,
                    DraftTenderObjectType.tender_id == tender.id,
                )
            )
        )

        object_group_name = query.scalars().first()

        return models.DraftTender(
            id=tender.id,
            user_id=tender.user_id,
            name=tender.name,
            price=tender.price,
            is_contract_price=tender.is_contract_price,
            is_nds_price=tender.is_nds_price,
            location=tender.city_id,
            floor_space=tender.floor_space,
            description=tender.description,
            wishes=tender.wishes,
            specification=tender.specification,
            attachments=tender.attachments,
            services_groups=list(services_groups_names.keys()),
            services_types=services_type_names,
            reception_start=tender.reception_start,
            reception_end=tender.reception_end,
            work_start=tender.work_start,
            work_end=tender.work_end,
            object_group=object_group_name,
            objects_types=objects_type_names,
            update_at=tender.update_at,
        )

    async def get_user_tenders(self, user_id: str) -> List[models.DraftTender]:
        query = await self.db.execute(
            select(DraftTender, City.name)
            .join(City)
            .where(DraftTender.user_id == user_id)
        )

        found_tenders = query.tuples().all()

        tenders: List[models.DraftTender] = []

        for found_tender in found_tenders:
            tender, city_name = found_tender

            tenders.append(
                await self.format_draft_tender(
                    tender=tender,
                )
            )

        return tenders
