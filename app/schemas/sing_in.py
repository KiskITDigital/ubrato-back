from pydantic import BaseModel, EmailStr


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignInResponse(BaseModel):
    access_token: str
