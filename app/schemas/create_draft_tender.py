from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CreateDraftTenderRequest(BaseModel):
    name: str
    price: Optional[int]
    is_contract_price: Optional[bool]
    is_nds_price: Optional[bool]
    floor_space: Optional[int]
    description: Optional[str]
    wishes: Optional[str]
    specification: Optional[str]
    attachments: Optional[List[str]]
    services_types: List[int]
    objects_types: List[int]
    reception_start: Optional[datetime]
    reception_end: Optional[datetime]
    work_start: Optional[datetime]
    work_end: Optional[datetime]
    city_id: Optional[int]
