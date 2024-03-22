from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

PhoneNumber.phone_format = "E164"


class User(BaseModel):
    id: str
    email: EmailStr
    phone: PhoneNumber
    password: str
    first_name: str
    middle_name: str
    last_name: str
    verified: bool
    role: int
    is_contractor: bool
    created_at: datetime


class UserPrivateDTO(BaseModel):
    id: str
    email: EmailStr
    phone: PhoneNumber
    first_name: str
    middle_name: str
    last_name: str
    verified: bool
    role: int
    is_contractor: bool
    created_at: datetime
