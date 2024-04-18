from typing import List, Optional

from pydantic import BaseModel


class Notification(BaseModel):
    id: int
    header: Optional[str]
    msg: Optional[str]
    href: Optional[str]
    read: bool


class Notifications(BaseModel):
    total: int
    notifications: List[Notification]
