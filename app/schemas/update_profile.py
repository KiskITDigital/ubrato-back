from typing import List

from pydantic import BaseModel


class UpdateCustomerProfileRequest(BaseModel):
    description: str
    locations: List[int]


class ContractorPricingRequest(BaseModel):
    id: int
    price: int


class ContractorCVRequest(BaseModel):
    name: str
    description: str
    imgs: List[str]


class UpdateContractorProfileRequest(BaseModel):
    description: str
    locations: List[int]
    services: List[ContractorPricingRequest]
    objects: List[int]


class UpdateBrandProfileRequest(BaseModel):
    name: str
    avatar: str
