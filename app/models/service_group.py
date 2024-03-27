from typing import List

from pydantic import BaseModel


class ServiceGroupModel(BaseModel):
    id: int
    name: str


class ServiceTypeModel(BaseModel):
    id: int
    name: str
    count: int = 0


class ServiceGroupWithTypes(BaseModel):
    id: int
    name: str
    types: List[ServiceTypeModel]
    total: int = 0


class ServicesGroupsWithTypes(BaseModel):
    groups: List[ServiceGroupWithTypes]
