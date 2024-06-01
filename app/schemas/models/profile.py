from typing import List, Optional

from pydantic import BaseModel


class ContractorPricing(BaseModel):
    id: int
    name: str
    price: int


class ProfileLocation(BaseModel):
    id: int
    name: str


class ContractorObject(BaseModel):
    id: int
    name: str


class ContractorCV(BaseModel):
    id: str
    name: str
    description: str
    links: List[str]


class CustomerProfile(BaseModel):
    description: Optional[str]
    locations: List[ProfileLocation]


class ContractorProfile(BaseModel):
    description: Optional[str]
    locations: List[ProfileLocation]
    services: List[ContractorPricing]
    objects: List[ContractorObject]
    portfolio: List[ContractorCV]
