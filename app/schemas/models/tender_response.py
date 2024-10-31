from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TenderResponse(BaseModel):
    company_id: str
    company_name: str
    company_avatar: Optional[str]
    price: Optional[int]
    response_at: datetime
