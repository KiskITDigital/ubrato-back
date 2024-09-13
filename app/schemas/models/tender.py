from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Category(BaseModel):
    name: str
    services: List[str]


class Tender(BaseModel):
    id: int
    name: str
    price: int
    is_contract_price: bool
    is_nds_price: bool
    location: str
    floor_space: int
    description: str
    wishes: str
    specification: str
    attachments: List[str]
    categories: List[Category]
    reception_start: datetime
    reception_end: datetime
    work_start: datetime
    work_end: datetime
    object_group: str
    objects_types: List[str]
    user_id: str
    created_at: datetime
    verified: bool


class DraftTender(BaseModel):
    id: int
    user_id: str
    name: str
    price: Optional[int]
    is_contract_price: Optional[bool]
    is_nds_price: Optional[bool]
    location: Optional[int]
    floor_space: Optional[int]
    description: Optional[str]
    wishes: Optional[str]
    specification: Optional[str]
    attachments: Optional[List[str]]
    services_groups: List[int]
    services_types: List[int]
    reception_start: Optional[datetime]
    reception_end: Optional[datetime]
    work_start: Optional[datetime]
    work_end: Optional[datetime]
    object_group: Optional[int]
    objects_types: List[int]
    update_at: Optional[datetime]
