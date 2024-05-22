from datetime import datetime

from pydantic import BaseModel


class TenderResponse(BaseModel):
    user_id: str
    tender_id: int
    response_at: datetime
