from typing import List, Optional

from config import get_config
from fastapi import Depends, status
from repositories.postgres import TagsRepository, TenderRepository
from repositories.postgres.schemas import Tender
from repositories.typesense.tender import TenderIndex
from schemas import models
from schemas.create_tender import CreateTenderRequest
from schemas.models import ObjectsGroupsWithTypes, ServicesGroupsWithTypes
from services.exceptions import ServiceException


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
        self.localization = get_config().Localization.config

    async def create_tender(
        self, tender: CreateTenderRequest, user_id: str
    ) -> models.Tender:
        # if len(tender.services_types) == 0:
        #     raise ServiceException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=self.localization["errors"]["invalid_services_count"],
        #     )

        # if len(tender.objects_types) == 0:
        #     raise ServiceException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=self.localization["errors"]["invalid_objects_count"],
        #     )

        created_tender = await self.tender_repository.create_tender(
            tender=Tender(
                name=tender.name,
                price=tender.price,
                is_contract_price=tender.is_contract_price,
                is_nds_price=tender.is_nds_price,
                city_id=tender.city_id,
                floor_space=tender.floor_space,
                description=tender.description,
                wishes=tender.wishes,
                specification=tender.specification,
                attachments=tender.attachments,
                reception_start=tender.reception_start,
                reception_end=tender.reception_end,
                work_start=tender.work_start,
                work_end=tender.work_end,
                user_id=user_id,
            ),
            service_type_ids=tender.services_types,
            object_type_ids=tender.objects_types,
        )

        self.tender_index.save(
            tender=created_tender.ConvertToIndexSchema(),
            services=tender.services_types,
            objects=tender.objects_types,
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

        self.tender_index.update(
            tender=updated_tender.ConvertToIndexSchema(),
            services=tender.services_types,
            objects=tender.objects_types,
        )

    async def respond_tender(
        self, tender_id: int, user_id: str, price: Optional[int]
    ) -> None:
        await self.tender_repository.respond_tender(
            tender_id=tender_id, user_id=user_id, price=price
        )

    async def is_responded(self, tender_id: int, user_id: str) -> bool:
        return await self.tender_repository.is_responded(
            tender_id=tender_id, user_id=user_id
        )

    async def is_has_offer(self, tender_id: int, org_id: str) -> bool:
        return await self.tender_repository.is_has_offer(
            tender_id=tender_id, org_id=org_id
        )

    async def make_offer(
        self, contractor_id: str, tender_id: int, user_id: str
    ) -> None:
        if not await self.has_permission_make_offer(
            user_id=user_id, tender_id=tender_id
        ):
            raise ServiceException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.localization["errors"]["no_access"],
            )

        if await self.is_already_got_offer(
            contractor_id=contractor_id, tender_id=tender_id
        ):
            raise ServiceException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.localization["errors"]["already_has_offer"],
            )

        await self.tender_repository.make_offer(
            contractor_id=contractor_id, tender_id=tender_id
        )

    async def is_already_got_offer(
        self, contractor_id: str, tender_id: int
    ) -> bool:
        return await self.tender_repository.is_offer_exist(
            contractor_id=contractor_id, tender_id=tender_id
        )

    async def has_permission_make_offer(
        self, user_id: str, tender_id: int
    ) -> bool:
        return await self.tender_repository.is_tender_owner(
            user_id=user_id, tender_id=tender_id
        )

    async def add_to_favorite(self, user_id: str, tender_id: int) -> None:
        await self.tender_repository.add_to_favorite(
            tender_id=tender_id, user_id=user_id
        )

    async def remove_from_favorite(self, user_id: str, tender_id: int) -> None:
        await self.tender_repository.remove_from_favorite(
            tender_id=tender_id, user_id=user_id
        )

    async def is_favorite(self, user_id: str, tender_id: int) -> bool:
        return await self.tender_repository.is_favorite(
            tender_id=tender_id, user_id=user_id
        )

    async def get_user_tenders(self, user_id: str) -> List[models.Tender]:
        return await self.tender_repository.get_user_tenders(user_id=user_id)

    async def get_tender_responses(self, tender_id: int) -> List[models.TenderResponse]:
        return await self.tender_repository.get_tender_responses(tender_id=tender_id)
