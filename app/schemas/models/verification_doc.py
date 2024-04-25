from pydantic import BaseModel


class VerificationDoc(BaseModel):
    id: str
    type: str
    link: str
