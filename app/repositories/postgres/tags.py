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
from repositories.postgres.database import get_db_connection
from repositories.postgres.schemas import (
    ObjectGroup,
    ObjectType,
    ServiceGroup,
    ServiceType,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TagsRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def get_all_objects_with_types(
        self,
    ) -> ObjectsGroupsWithTypes:
        object_groups = await self.db.execute(select(ObjectGroup))

        groups_data: List[ObjectGroupWithTypes] = []

        for group in object_groups:
            query = await self.db.execute(
                select(ObjectType).where(
                    ObjectType.object_group_id == group.id
                )
            )

            types_in_group = query.all()

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

    async def get_all_services_with_types(
        self,
    ) -> ServicesGroupsWithTypes:
        service_groups = await self.db.execute(select(ServiceGroup))

        groups_data: List[ServiceGroupWithTypes] = []

        for group in service_groups:
            query = await self.db.execute(
                select(ServiceType).where(
                    ServiceType.service_group_id == group.id
                )
            )

            types_in_group = query.all()

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
