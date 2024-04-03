from typing import List, Optional

import models
from fastapi import Depends
from models import ObjectsGroupsWithTypes, ServicesGroupsWithTypes
from repositories import TagsRepository, TenderRepository
from repositories.schemas import Tender
from schemas.create_tender import CreateTenderRequest


class TenderService:
    tags_repository: TagsRepository
    tender_repository: TenderRepository

    def __init__(
        self,
        tags_repository: TagsRepository = Depends(),
        tender_repository: TenderRepository = Depends(),
    ) -> None:
        self.tags_repository = tags_repository
        self.tender_repository = tender_repository

    def create_tender(
        self, tender: CreateTenderRequest, user_id: str
    ) -> models.Tender:
        created_tender = self.tender_repository.create_tender(
            Tender(**tender.__dict__, user_id=user_id)
        )
        return self.tender_repository.get_tender_by_id(
            tender_id=created_tender.id
        )

    def get_page_tenders(
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
        text: Optional[str],
        active: Optional[bool],
        verified: Optional[bool],
        user_id: Optional[str],
    ) -> List[models.Tender]:
        return self.tender_repository.get_page_tenders(
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
            text=text,
            active=active,
            verified=verified,
            user_id=user_id,
        )

    def get_all_objects_with_types(
        self,
    ) -> ObjectsGroupsWithTypes:
        objects = self.tags_repository.get_all_objects_with_types()

        for group in objects.groups:
            total = 0
            for type in group.types:
                count = self.tender_repository.get_count_active_tenders(
                    object_group_id=type.id, service_type_id=None
                )
                type.count = count
                total += count
            group.total = total

        return objects

    def get_all_services_with_types(
        self,
    ) -> ServicesGroupsWithTypes:
        services = self.tags_repository.get_all_services_with_types()

        for group in services.groups:
            total = 0
            for type in group.types:
                count = self.tender_repository.get_count_active_tenders(
                    object_group_id=None, service_type_id=type.id
                )
                type.count = count
                total += count
            group.total = total

        return services

    def get_count_active_tenders(
        self,
        object_group_id: Optional[int],
        service_type_id: Optional[int],
    ) -> int:
        return self.tender_repository.get_count_active_tenders(
            object_group_id=object_group_id, service_type_id=service_type_id
        )

    def get_by_id(self, tender_id: int) -> models.Tender:
        return self.tender_repository.get_tender_by_id(tender_id=tender_id)

    def update_tender(
        self, tender: CreateTenderRequest, tender_id: int
    ) -> None:
        self.tender_repository.update_tender(
            tender=tender.__dict__,
            tender_id=tender_id,
        )
