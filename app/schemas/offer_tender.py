from pydantic import BaseModel


class OfferTenderRequest(BaseModel):
    tender_id: int
