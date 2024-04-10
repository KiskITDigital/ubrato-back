from datetime import datetime
from typing import Any, List, Optional

import models
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import (
    TENDERID_NOT_FOUND,
    RepositoryException,
)
from repositories.postgres.schemas import (
    City,
    ObjectGroup,
    ObjectType,
    ServiceGroup,
    ServiceType,
    Tender,
    TenderServiceGroup,
    TenderServiceType,
)
from sqlalchemy import and_, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class TenderRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def create_tender(
        self,
        tender: Tender,
        service_type_ids: List[int],
        service_group_ids: List[int],
    ) -> Tender:
        self.db.add(tender)
        await self.db.flush()
        for id in service_type_ids:
            self.db.add(
                TenderServiceType(
                    tender_id=tender.id,
                    service_type_id=id,
                )
            )
            await self.db.flush()
        for id in service_group_ids:
            self.db.add(
                TenderServiceGroup(
                    tender_id=tender.id,
                    service_group_id=id,
                )
            )
            await self.db.flush()
        await self.db.commit()

        await self.db.refresh(tender)

        return tender

    async def update_tender(
        self, tender: dict[str, Any], tender_id: int
    ) -> Tender:
        query = await self.db.execute(
            select(Tender).where(Tender.id == tender_id)
        )

        tender_to_update = query.scalar()

        if tender_to_update is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=tender_id,
                sql_msg="",
            )

        for key, value in tender.items():
            setattr(tender_to_update, key, value)
            tender_to_update.verified = False

        await self.db.execute(
            delete(TenderServiceGroup).where(
                TenderServiceGroup.tender_id == tender_to_update.id,
            )
        )

        await self.db.execute(
            delete(TenderServiceType).where(
                TenderServiceType.tender_id == tender_to_update.id,
            )
        )

        await self.db.flush()

        for id in tender["services_types"]:
            self.db.add(
                TenderServiceType(
                    tender_id=tender_to_update.id,
                    service_type_id=id,
                )
            )

        for id in tender["services_groups"]:
            self.db.add(
                TenderServiceGroup(
                    tender_id=tender_to_update.id,
                    service_group_id=id,
                )
            )

        await self.db.commit()
        await self.db.refresh(tender_to_update)
        return tender_to_update

    async def get_page_tenders(
        self,
        page: int,
        page_size: int,
        object_group_id: Optional[int],
        object_type_id: Optional[int],
        service_type_ids: Optional[List[int]],
        service_group_ids: Optional[List[int]],
        floor_space_from: Optional[int],
        floor_space_to: Optional[int],
        price_from: Optional[int],
        price_to: Optional[int],
        verified: Optional[bool],
        user_id: Optional[str],
    ) -> List[models.Tender]:
        reception_end_condition = Tender.reception_end > datetime.now()

        object_group_condition = (object_group_id is None) or (
            Tender.object_group_id == object_group_id
        )

        object_type_condition = (object_type_id is None) or (
            Tender.object_type_id == object_type_id
        )

        service_type_condition = (service_type_ids is None) or and_(
            *(
                Tender.services_types.any(service_type_id)  # type: ignore
                for service_type_id in service_type_ids
            )
        )

        service_group_condition = (service_group_ids is None) or and_(
            *(
                Tender.services_groups.any(service_group_id)  # type: ignore
                for service_group_id in service_group_ids
            )
        )

        floor_space_from_condition = (floor_space_from is None) or (
            Tender.floor_space >= floor_space_from
        )

        floor_space_to_condition = (floor_space_to is None) or (
            Tender.floor_space <= floor_space_to
        )

        price_from_condition = (price_from is None) or (
            Tender.price >= price_from
        )

        price_to_condition = (price_to is None) or (Tender.price <= price_to)

        verified_condition = (verified is None) or (
            Tender.verified == verified
        )

        user_id_condition = (user_id is None) or (Tender.user_id == user_id)

        query = await self.db.execute(
            select(Tender, ObjectGroup.name, ObjectType.name, City.name)
            .join(ObjectGroup, Tender.object_group_id == ObjectGroup.id)
            .join(ObjectType, Tender.object_type_id == ObjectType.id)
            .join(City, Tender.city_id == City.id)
            .where(
                and_(
                    reception_end_condition,
                    object_group_condition,  # type: ignore
                    object_type_condition,  # type: ignore
                    service_type_condition,  # type: ignore
                    service_group_condition,  # type: ignore
                    floor_space_from_condition,  # type: ignore
                    floor_space_to_condition,  # type: ignore
                    price_from_condition,  # type: ignore
                    price_to_condition,  # type: ignore
                    verified_condition,  # type: ignore
                    user_id_condition,  # type: ignore
                )
            )
            .order_by(Tender.created_at.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        tenders: List[models.Tender] = []

        for found_tender in query.all():
            tender, object_group_name, object_type_name, city_name = (
                found_tender._tuple()
            )

            tender_model = await self.format_tender(
                tender=tender,
                object_group_name=object_group_name,
                object_type_name=object_type_name,
                city_name=city_name,
            )
            tenders.append(tender_model)

        return tenders

    async def get_tender_by_id(self, tender_id: int) -> models.Tender:
        query = await self.db.execute(
            select(Tender, ObjectGroup.name, ObjectType.name, City.name)
            .join(City)
            .join(ObjectGroup)
            .join(ObjectType)
            .where(Tender.id == tender_id)
        )

        found_tender = query.tuples().first()

        if found_tender is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=TENDERID_NOT_FOUND.format(tender_id),
                sql_msg="",
            )

        tender, object_group_name, object_type_name, city_name = found_tender

        return await self.format_tender(
            tender=tender,
            object_group_name=object_group_name,
            object_type_name=object_type_name,
            city_name=city_name,
        )

    async def update_verified_status(
        self, tender_id: int, verified: bool
    ) -> None:
        query = await self.db.execute(
            select(Tender).where(Tender.id == tender_id)
        )

        tender = query.scalar()

        if tender is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=TENDERID_NOT_FOUND.format(tender_id),
                sql_msg="",
            )

        tender.verified = verified
        await self.db.commit()

    async def get_count_active_tenders(
        self, object_group_id: Optional[int], service_type_ids: Optional[int]
    ) -> int:
        stmn = select(func.count(Tender.id))
        if object_group_id:
            stmn.where(Tender.object_group_id == object_group_id)

        if service_type_ids:
            stmn.join(Tender.id == TenderServiceGroup.tender_id).where(
                TenderServiceGroup.service_group_id == service_type_ids
            )

        query = await self.db.execute(stmn)
        result = query.scalar()
        if result is None:
            result = 0
        return result

    async def format_tender(
        self,
        tender: Tender,
        object_group_name: str,
        object_type_name: str,
        city_name: str,
    ) -> models.Tender:
        services_groups_names: List[str] = []

        query = await self.db.execute(
            select(ServiceGroup.name)
            .join(
                TenderServiceGroup,
                TenderServiceGroup.service_group_id == ServiceGroup.id,
            )
            .where(TenderServiceGroup.tender_id == tender.id)
        )

        services_groups = query.scalars()

        for name in services_groups:
            services_groups_names.append(name)

        services_type_names: List[str] = []

        query = await self.db.execute(
            select(ServiceType.name)
            .join(
                TenderServiceType,
                TenderServiceType.service_type_id == ServiceType.id,
            )
            .where(TenderServiceType.tender_id == tender.id)
        )

        services_types = query.scalars()

        for name in services_types:
            services_type_names.append(name)

        return models.Tender(
            id=tender.id,
            name=tender.name,
            price=tender.price,
            is_contract_price=tender.is_contract_price,
            location=city_name,
            floor_space=tender.floor_space,
            description=tender.description,
            wishes=tender.wishes,
            attachments=tender.attachments,
            services_groups=services_groups_names,
            services_types=services_type_names,
            reception_start=tender.reception_start,
            reception_end=tender.reception_end,
            work_start=tender.work_start,
            work_end=tender.work_end,
            object_group_id=object_group_name,
            object_type_id=object_type_name,
            user_id=tender.user_id,
            created_at=tender.created_at,
            verified=tender.verified,
            active=tender.active,
        )
