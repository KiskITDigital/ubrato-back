from typing import List

from pydantic import BaseModel


class ServiceGroupModel(BaseModel):
    id: int
    name: str


class ServiceTypeModel(BaseModel):
    id: int
    name: str
    count: int = None


class ServiceGroupWithTypes(BaseModel):
    id: int
    name: str
    types: List[ServiceTypeModel]
    total: int = None


class ServicesGroupsWithTypes(BaseModel):
    groups: List[ServiceGroupWithTypes]
