from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VerificationInfo(BaseModel):
    id: str
    verified: Optional[bool]
    msg: Optional[str]
    verified_at: Optional[datetime]
    created_at: datetime
