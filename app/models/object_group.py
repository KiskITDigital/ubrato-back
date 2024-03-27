from typing import List

from pydantic import BaseModel


class ObjectTypeModel(BaseModel):
    id: int
    name: str
    count: int = 0


class ObjectGroupModel(BaseModel):
    id: int
    name: str


class ObjectGroupWithTypes(BaseModel):
    id: int
    name: str
    total: int = 0
    types: List[ObjectTypeModel]


class ObjectsGroupsWithTypes(BaseModel):
    groups: List[ObjectGroupWithTypes]
