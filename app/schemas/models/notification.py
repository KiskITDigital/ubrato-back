from typing import List, Optional

from pydantic import BaseModel


class Notification(BaseModel):
    msg: str
    href: Optional[str]


class Notifications(BaseModel):
    total: int
    notifications: List[Notification]
