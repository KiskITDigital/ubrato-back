from models.user_model import User
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

PhoneNumber.phone_format = "E164"


class SignUpRequest(BaseModel):
    brand_name: str
    inn: int
    email: EmailStr
    phone: PhoneNumber
    password: str
    first_name: str
    middle_name: str
    last_name: str

class SignUpResponse(BaseModel):
    status: bool
