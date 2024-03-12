from typing import List
from pydantic import BaseModel

class ObjectTypeModel(BaseModel):
    id: int
    name: str

class ObjectGroupModel(BaseModel):
    id: int
    name: str

class ObjectGroupWithTypes(BaseModel):
    id: int
    name: str
    types: List[ObjectTypeModel]

class ObjectsGroupsWithTypes(BaseModel):
    groups: List[ObjectGroupWithTypes]
