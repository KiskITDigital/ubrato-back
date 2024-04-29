from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from .organization import OrganizationLiteDTO

PhoneNumber.phone_format = "E164"


class User(BaseModel):
    id: str
    email: EmailStr
    phone: PhoneNumber
    password: str
    totp_salt: str
    first_name: str
    middle_name: str
    last_name: str
    avatar: str
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
    avatar: str
    verified: bool
    role: int
    is_contractor: bool
    created_at: datetime


class UserMe(BaseModel):
    id: str
    email: EmailStr
    phone: PhoneNumber
    first_name: str
    middle_name: str
    last_name: str
    avatar: str
    verified: bool
    role: int
    is_contractor: bool
    organiztion: OrganizationLiteDTO
    created_at: datetime
