from typing import List, Optional

from pydantic import BaseModel


class CustomerProfile(BaseModel):
    description: Optional[str]
    locations: List[str]


class ContractorPricing(BaseModel):
    name: str
    price: int


class ContractorCV(BaseModel):
    name: str
    description: str
    links: List[str]


class ContractorProfile(BaseModel):
    description: Optional[str]
    locations: List[str]
    services: List[ContractorPricing]
    portfolio: List[ContractorCV]
