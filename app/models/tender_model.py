from datetime import datetime
from typing import List

from pydantic import BaseModel


class Tender(BaseModel):
    id: str
    name: str
    price: int
    is_contract_price: bool
    regions: List[str]
    floor_space: int
    description: str
    wishes: str
    attachments: List[str]
    services_groups: List[int]
    services_types: List[int]
    active: bool
    reception_start: datetime
    reception_end: datetime
    work_start: datetime
    work_end: datetime
    object_group_id: int
    object_type_id: int
    user_id: str
    created_at: datetime
