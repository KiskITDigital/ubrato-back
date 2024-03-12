from typing import List
from pydantic import BaseModel

class ServiceGroupModel(BaseModel):
    id: int
    name: str

class ServiceTypeModel(BaseModel):
    id: int
    name: str

class ServiceGroupWithTypes(BaseModel):
    id: int
    name: str
    types: List[ServiceTypeModel]

class ServicesGroupsWithTypes(BaseModel):
    groups: List[ServiceGroupWithTypes]
