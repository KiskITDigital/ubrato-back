from typing import List

from pydantic import BaseModel


class VerifyRequest(BaseModel):
    org_id: str
    documents: List[str]
