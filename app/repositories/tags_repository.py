from typing import List

from fastapi import Depends
from models import (
    ObjectGroupWithTypes,
    ObjectsGroupsWithTypes,
    ObjectTypeModel,
    ServiceGroupWithTypes,
    ServicesGroupsWithTypes,
    ServiceTypeModel,
)
from repositories.database import get_db_connection
from repositories.exceptions import RepositoryException
from repositories.schemas import (
    ObjectGroup,
    ObjectType,
    ServiceGroup,
    ServiceType,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session


class TagsRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def get_all_objects_with_types(
        self,
    ) -> ObjectsGroupsWithTypes:
        try:
            object_groups = self.db.query(ObjectGroup)

            groups_data: List[ObjectGroupWithTypes] = []

            for group in object_groups:
                types_in_group = (
                    self.db.query(ObjectType)
                    .filter(ObjectType.object_group_id == group.id)
                    .all()
                )
                types_list = [
                    ObjectTypeModel(id=obj_type.id, name=obj_type.name)
                    for obj_type in types_in_group
                ]
                groups_data.append(
                    ObjectGroupWithTypes(
                        id=group.id, name=group.name, types=types_list
                    )
                )

            return ObjectsGroupsWithTypes(groups=groups_data)

        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def get_all_services_with_types(
        self,
    ) -> ObjectsGroupsWithTypes:
        try:
            service_groups = self.db.query(ServiceGroup)

            groups_data: List[ServicesGroupsWithTypes] = []

            for group in service_groups:
                types_in_group = (
                    self.db.query(ServiceType)
                    .filter(ServiceType.service_group_id == group.id)
                    .all()
                )
                types_list = [
                    ServiceTypeModel(id=obj_type.id, name=obj_type.name)
                    for obj_type in types_in_group
                ]
                groups_data.append(
                    ServiceGroupWithTypes(
                        id=group.id, name=group.name, types=types_list
                    )
                )

            return ServicesGroupsWithTypes(groups=groups_data)

        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )
