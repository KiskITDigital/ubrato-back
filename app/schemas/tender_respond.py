from typing import Optional

from pydantic import BaseModel


class TenderRespondRequest(BaseModel):
    price: Optional[int]
