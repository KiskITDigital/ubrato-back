from typing import List, Optional, Tuple

from fastapi import Depends
from models.object_group import ObjectsGroupsWithTypes
from models.service_group import ServicesGroupsWithTypes
from repositories.tags_repository import TagsRepository


class TenderService:
    tags_repository: TagsRepository

    def __init__(self, tags_repository: TagsRepository = Depends()) -> None:
        self.tags_repository = tags_repository

    def get_all_objects_with_types(self) -> Tuple[ObjectsGroupsWithTypes, Optional[Exception]]:
        return self.tags_repository.get_all_objects_with_types()
    
    def get_all_services_with_types(self) -> Tuple[ServicesGroupsWithTypes, Optional[Exception]]:
        return self.tags_repository.get_all_services_with_types()