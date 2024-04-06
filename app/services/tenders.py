from typing import List, Optional

import models
from fastapi import Depends
from models import ObjectsGroupsWithTypes, ServicesGroupsWithTypes
from repositories.postgres import TagsRepository, TenderRepository
from repositories.postgres.schemas import Tender
from repositories.typesense.schemas import TypesenseTender
from repositories.typesense.tender import TenderIndex
from schemas.create_tender import CreateTenderRequest


class TenderService:
    tags_repository: TagsRepository
    tender_repository: TenderRepository

    def __init__(
        self,
        tags_repository: TagsRepository = Depends(),
        tender_repository: TenderRepository = Depends(),
        tender_index: TenderIndex = Depends(),
    ) -> None:
        self.tags_repository = tags_repository
        self.tender_repository = tender_repository
        self.tender_index = tender_index

    async def create_tender(
        self, tender: CreateTenderRequest, user_id: str
    ) -> models.Tender:
        created_tender = await self.tender_repository.create_tender(
            Tender(**tender.__dict__, user_id=user_id)
        )
        self.tender_index.save(
            tender=TypesenseTender(
                id=str(created_tender.id),
                name=created_tender.name,
                price=created_tender.price,
                is_contract_price=created_tender.is_contract_price,
                city_id=created_tender.city_id,
                floor_space=created_tender.floor_space,
                description=created_tender.description,
                wishes=created_tender.wishes,
                services_groups=created_tender.services_groups,
                services_types=created_tender.services_types,
                reception_start=int(
                    created_tender.reception_start.timestamp()
                ),
                reception_end=int(created_tender.reception_end.timestamp()),
                work_start=int(created_tender.work_start.timestamp()),
                work_end=int(created_tender.work_end.timestamp()),
                object_group_id=created_tender.object_group_id,
                object_type_id=created_tender.object_type_id,
                verified=created_tender.verified,
                active=created_tender.active,
                created_at=int(created_tender.created_at.timestamp()),
            )
        )
        return await self.tender_repository.get_tender_by_id(
            tender_id=created_tender.id
        )

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
        return await self.tender_repository.get_page_tenders(
            page=page,
            page_size=page_size,
            object_group_id=object_group_id,
            object_type_id=object_type_id,
            service_type_ids=service_type_ids,
            service_group_ids=service_group_ids,
            floor_space_from=floor_space_from,
            floor_space_to=floor_space_to,
            price_from=price_from,
            price_to=price_to,
            verified=verified,
            user_id=user_id,
        )

    async def get_all_objects_with_types(
        self,
    ) -> ObjectsGroupsWithTypes:
        objects = await self.tags_repository.get_all_objects_with_types()

        for group in objects.groups:
            total = 0
            for type in group.types:
                count = await self.tender_repository.get_count_active_tenders(
                    object_group_id=type.id, service_type_ids=None
                )
                type.count = count
                total += count
            group.total = total

        return objects

    async def get_all_services_with_types(
        self,
    ) -> ServicesGroupsWithTypes:
        services = await self.tags_repository.get_all_services_with_types()

        for group in services.groups:
            total = 0
            for type in group.types:
                count = await self.tender_repository.get_count_active_tenders(
                    object_group_id=None, service_type_ids=type.id
                )
                type.count = count
                total += count
            group.total = total

        return services

    async def get_count_active_tenders(
        self,
        object_group_id: Optional[int],
        service_type_id: Optional[int],
    ) -> int:
        return await self.tender_repository.get_count_active_tenders(
            object_group_id=object_group_id, service_type_ids=service_type_id
        )

    async def get_by_id(self, tender_id: int) -> models.Tender:
        return await self.tender_repository.get_tender_by_id(
            tender_id=tender_id
        )

    async def update_tender(
        self, tender: CreateTenderRequest, tender_id: int
    ) -> None:
        await self.tender_repository.update_tender(
            tender=tender.__dict__,
            tender_id=tender_id,
        )
