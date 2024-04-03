from datetime import datetime
from typing import List

from pydantic import BaseModel


class Tender(BaseModel):
    id: int
    name: str
    price: int
    is_contract_price: bool
    location: str
    floor_space: int
    description: str
    wishes: str
    attachments: List[str]
    services_groups: List[str]
    services_types: List[str]
    active: bool
    reception_start: datetime
    reception_end: datetime
    work_start: datetime
    work_end: datetime
    object_group_id: str
    object_type_id: str
    user_id: str
    created_at: datetime
    verified: bool
