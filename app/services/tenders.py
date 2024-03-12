from typing import Optional, Tuple
import uuid

from fastapi import Depends
from models.object_group import ObjectsGroupsWithTypes
from models.service_group import ServicesGroupsWithTypes
from repositories.schemas import Tender
from repositories.tags_repository import TagsRepository
from schemas.create_tender import CreateTenderRequest


class TenderService:
    tags_repository: TagsRepository

    def __init__(self, tags_repository: TagsRepository = Depends()) -> None:
        self.tags_repository = tags_repository

    def create_tender(self, tender: CreateTenderRequest, user_id: str) -> Tuple[str, Optional[Exception]]:
        id = "ten_" + str(uuid.uuid4())

        err = self.tags_repository.create_tender(Tender(**tender.__dict__, id=id, user_id=user_id))
        return id, err

    def get_all_objects_with_types(self) -> Tuple[ObjectsGroupsWithTypes, Optional[Exception]]:
        return self.tags_repository.get_all_objects_with_types()
    
    def get_all_services_with_types(self) -> Tuple[ServicesGroupsWithTypes, Optional[Exception]]:
        return self.tags_repository.get_all_services_with_types()