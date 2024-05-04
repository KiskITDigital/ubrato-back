from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Notification(BaseModel):
    id: int
    header: Optional[str]
    msg: Optional[str]
    href: Optional[str]
    href_text: Optional[str]
    href_color: Optional[int]
    read: bool
    created_at: datetime


class Notifications(BaseModel):
    total: int
    notifications: List[Notification]
