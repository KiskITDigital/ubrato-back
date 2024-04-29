from pydantic import BaseModel


class ChangePasswordRequest(BaseModel):
    email: str
    code: str
    password: str
