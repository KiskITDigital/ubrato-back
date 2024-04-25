from pydantic import BaseModel


class VerificationDocType(BaseModel):
    id: int
    name: str
