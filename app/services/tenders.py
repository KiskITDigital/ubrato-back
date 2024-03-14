import uuid
from typing import List, Optional, Tuple

import models
from fastapi import Depends
from models.object_group import ObjectsGroupsWithTypes
from models.service_group import ServicesGroupsWithTypes
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
    ) -> Tuple[str, Optional[Exception]]:
        id = "ten_" + str(uuid.uuid4())

        err = self.tender_repository.create_tender(
            Tender(**tender.__dict__, id=id, user_id=user_id)
        )
        return id, err

    def get_page_active_tenders(
        self,
        page: int,
        page_size: int,
    ) -> Tuple[List[models.Tender], Optional[Exception]]:
        return self.tender_repository.get_page_active_tenders(
            page=page, page_size=page_size
        )

    def get_all_objects_with_types(
        self,
    ) -> Tuple[ObjectsGroupsWithTypes, Optional[Exception]]:
        return self.tags_repository.get_all_objects_with_types()

    def get_all_services_with_types(
        self,
    ) -> Tuple[ServicesGroupsWithTypes, Optional[Exception]]:
        return self.tags_repository.get_all_services_with_types()
