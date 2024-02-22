from typing import List

from pydantic import BaseModel


class VerifyRequest(BaseModel):
    brand_name: str
    short_name: str
    inn: int
    okpo: int
    orgn: int
    kpp: int
    tax_code: int
    real_address: str
    registered_address: str
    mail_address: str
    documents: List[str]
