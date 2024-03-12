from typing import List, Optional, Tuple
from fastapi import Depends

from sqlalchemy.orm import scoped_session
from models.object_group import ObjectGroupWithTypes, ObjectsGroupsWithTypes, ObjectTypeModel
from models.service_group import ServiceGroupWithTypes, ServiceTypeModel, ServicesGroupsWithTypes
from repositories.database import get_db_connection
from repositories.schemas import ObjectGroup, ObjectType, ServiceGroup, ServiceType, Tender
from sqlalchemy.exc import SQLAlchemyError


class TagsRepository:
    db: scoped_session

    def __init__(self, db: scoped_session = Depends(get_db_connection)) -> None:
        self.db = db

    def create_tender(
        self, tender: Tender
    ) -> Optional[Exception]:
        try:
            self.db.add(tender)
            self.db.commit()

            return None
        except SQLAlchemyError as err:
            print(err._sql_message)
            return Exception(err.code)

    def get_all_objects_with_types(
        self,
    ) -> Tuple[ObjectsGroupsWithTypes, Optional[Exception]]:
        try:
            object_groups = self.db.query(ObjectGroup)

            groups_data: List[ObjectGroupWithTypes] = []

            for group in object_groups:
                types_in_group = self.db.query(ObjectType).filter(ObjectType.object_group_id == group.id).all()
                types_list = [ObjectTypeModel(id=obj_type.id, name=obj_type.name) for obj_type in types_in_group]
                groups_data.append(ObjectGroupWithTypes(id=group.id, name=group.name, types=types_list))

            
            return ObjectsGroupsWithTypes(groups=groups_data), None

        except SQLAlchemyError as err:
            return [], Exception(err.code)
        
    def get_all_services_with_types(
        self,
    ) -> Tuple[ObjectsGroupsWithTypes, Optional[Exception]]:
        try:
            service_groups = self.db.query(ServiceGroup)

            groups_data: List[ServicesGroupsWithTypes] = []

            for group in service_groups:
                types_in_group = self.db.query(ServiceType).filter(ServiceType.service_group_id == group.id).all()
                types_list = [ServiceTypeModel(id=obj_type.id, name=obj_type.name) for obj_type in types_in_group]
                groups_data.append(ServiceGroupWithTypes(id=group.id, name=group.name, types=types_list))

            
            return ServicesGroupsWithTypes(groups=groups_data), None

        except SQLAlchemyError as err:
            return [], Exception(err.code)