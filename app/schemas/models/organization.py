from datetime import datetime

from pydantic import BaseModel


class Organization(BaseModel):
    id: str
    brand_name: str
    short_name: str
    inn: str
    okpo: str
    ogrn: str
    kpp: str
    tax_code: int
    address: str
    user_id: str
    update_at: datetime
    created_at: datetime


class OrganizationLiteDTO(BaseModel):
    id: str
    short_name: str
    inn: str
    okpo: str
    ogrn: str
    kpp: str
