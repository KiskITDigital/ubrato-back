from typing import List

from pydantic import BaseModel


class ObjectTypeModel(BaseModel):
    id: int
    name: str
    count: int = None


class ObjectGroupModel(BaseModel):
    id: int
    name: str


class ObjectGroupWithTypes(BaseModel):
    id: int
    name: str
    total: int = None
    types: List[ObjectTypeModel]


class ObjectsGroupsWithTypes(BaseModel):
    groups: List[ObjectGroupWithTypes]
