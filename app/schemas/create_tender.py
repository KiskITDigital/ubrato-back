from datetime import datetime
from typing import List

from pydantic import BaseModel


class CreateTenderRequest(BaseModel):
    name: str
    price: int
    is_contract_price: bool
    is_nds_price: bool
    floor_space: int
    description: str
    wishes: str
    specification: str
    attachments: List[str]
    services_types: List[int]
    objects_types: List[int]
    reception_start: datetime
    reception_end: datetime
    work_start: datetime
    work_end: datetime
    city_id: int
