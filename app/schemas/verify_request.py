from pydantic import BaseModel


class SaveVerificationDoc(BaseModel):
    link: str
    type: int
