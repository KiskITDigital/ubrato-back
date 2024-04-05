from typing import List

from pydantic import BaseModel


class TypesenseTender(BaseModel):
    id: str
    name: str
    price: int
    is_contract_price: bool
    city_id: int
    floor_space: int
    description: str
    wishes: str
    services_groups: List[int]
    services_types: List[int]
    reception_start: int
    reception_end: int
    work_start: int
    work_end: int
    object_group_id: int
    object_type_id: int
    verified: bool
    created_at: int
