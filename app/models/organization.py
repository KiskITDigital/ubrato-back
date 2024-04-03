from pydantic import BaseModel


class OrganizationLiteDTO(BaseModel):
    id: str
    short_name: str
    inn: str
