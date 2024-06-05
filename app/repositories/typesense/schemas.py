from pydantic import BaseModel


class TypesenseTender(BaseModel):
    id: str
    name: str
    price: int
    is_contract_price: bool
    is_nds_price: bool
    city_id: str
    floor_space: int
    description: str
    wishes: str
    reception_start: int
    reception_end: int
    work_start: int
    work_end: int
    user_id: str
    verified: bool
    created_at: int


class TypesenseContractor(BaseModel):
    id: str
    name: str
    inn: str


class TypesenseContractorService(BaseModel):
    contractor_id: str
    service_type_id: str
    price: int
