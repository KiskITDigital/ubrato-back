from typing import List, Optional

from fastapi import Depends
from repositories.postgres import TagsRepository, TenderRepository
from repositories.postgres.schemas import Tender
from repositories.typesense.tender import TenderIndex
from schemas import models
from schemas.create_tender import CreateTenderRequest
from schemas.models import ObjectsGroupsWithTypes, ServicesGroupsWithTypes


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
            tender=Tender(
                name=tender.name,
                price=tender.price,
                is_contract_price=tender.is_contract_price,
                city_id=tender.city_id,
                floor_space=tender.floor_space,
                description=tender.description,
                wishes=tender.wishes,
                attachments=tender.attachments,
                reception_start=tender.reception_start,
                reception_end=tender.reception_end,
                work_start=tender.work_start,
                work_end=tender.work_end,
                object_type_id=tender.object_type_id,
                user_id=user_id,
            ),
            service_type_ids=tender.services_types,
        )

        object_group_ids = await self.tender_repository.get_object_group(
            object_type_id=tender.object_type_id
        )

        services_groups_ids = await self.tender_repository.get_services_groups(
            service_type_ids=tender.services_types
        )

        self.tender_index.save(
            created_tender.ConvertToIndexSchema(
                object_group_id=object_group_ids,
                services_groups=services_groups_ids,
                services_types=tender.services_types,
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
                    object_type_id=type.id, service_type_ids=None
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
                    object_type_id=None, service_type_ids=type.id
                )
                type.count = count
                total += count
            group.total = total

        return services

    async def get_count_active_tenders(
        self,
        object_type_id: Optional[int],
        service_type_id: Optional[int],
    ) -> int:
        return await self.tender_repository.get_count_active_tenders(
            object_type_id=object_type_id, service_type_ids=service_type_id
        )

    async def get_by_id(self, tender_id: int) -> models.Tender:
        return await self.tender_repository.get_tender_by_id(
            tender_id=tender_id
        )

    async def update_tender(
        self, tender: CreateTenderRequest, tender_id: int
    ) -> None:
        updated_tender = await self.tender_repository.update_tender(
            tender=tender.__dict__,
            tender_id=tender_id,
        )

        object_group_ids = await self.tender_repository.get_object_group(
            object_type_id=tender.object_type_id
        )

        services_groups_ids = await self.tender_repository.get_services_groups(
            service_type_ids=tender.services_types
        )

        self.tender_index.update(
            updated_tender.ConvertToIndexSchema(
                object_group_id=object_group_ids,
                services_groups=services_groups_ids,
                services_types=tender.services_types,
            )
        )
