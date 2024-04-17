from pydantic import BaseModel


class VerifyStatusSet(BaseModel):
    status: bool
    message: str
