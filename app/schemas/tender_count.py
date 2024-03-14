from pydantic import BaseModel


class TenderCountResponse(BaseModel):
    count: int
