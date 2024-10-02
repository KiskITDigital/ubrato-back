from typing import List

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber
from schemas.models.organization import ContactInfo

PhoneNumber.phone_format = "E164"


class UpdateCustomerProfileRequest(BaseModel):
    description: str
    locations: List[int]


class ContractorPricingRequest(BaseModel):
    id: int
    price: int


class ContractorCVRequest(BaseModel):
    name: str
    description: str
    links: List[str]


class ContractorCVResponse(BaseModel):
    id: str


class UpdateContractorProfileRequest(BaseModel):
    description: str
    locations: List[int]
    services: List[ContractorPricingRequest]
    objects: List[int]


class UpdateBrandProfileRequest(BaseModel):
    name: str
    avatar: str


class UpdateBrandContactRequest(BaseModel):
    emails: List[ContactInfo]
    phones: List[ContactInfo]
    messengers: List[ContactInfo]


class UpdAvatarRequest(BaseModel):
    avatar: str


class UpdateUserInfoRequest(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone: PhoneNumber
