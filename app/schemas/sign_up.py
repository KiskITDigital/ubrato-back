from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

PhoneNumber.phone_format = "E164"


class SignUpRequest(BaseModel):
    email: EmailStr
    phone: PhoneNumber
    password: str
    first_name: str
    middle_name: str
    last_name: str
    avatar: str
    inn: str
    is_contractor: bool


class SignUpResponse(BaseModel):
    access_token: str
