from datetime import datetime
from typing import List

from pydantic import BaseModel


class CreateTenderRequest(BaseModel):
    name: str
    regions: List[str]
    floor_space: int
    description: str
    wishes: str
    attachments: List[str]
    services_groups: List[int]
    services_types: List[int]
    reception_start: datetime
    reception_end: datetime
    work_start: datetime
    work_end: datetime
    object_group_id: int
    object_type_id: int


class CreateTenderResponse(BaseModel):
    id: str
