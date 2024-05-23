from pydantic import BaseModel


class FavoriteContractor(BaseModel):
    id: str
    org_name: str
