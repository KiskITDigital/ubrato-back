import uuid
from typing import List, Optional

from config import get_config
from dadata import Dadata
from fastapi import Depends
from repositories import OrganizationRepository
from repositories.schemas import Document, Organization


class OrganizationService:
    org_repository: OrganizationRepository

    def __init__(
        self, org_repository: OrganizationRepository = Depends()
    ) -> None:
        self.org_repository = org_repository
        self.dadata = Dadata(get_config().Dadata.api_key)

    def get_organization(self, inn: str) -> Optional[Organization]:
        id = "org_" + str(uuid.uuid4())

        result = self.dadata.find_by_id("party", inn)

        if len(result) == 0:
            return None

        org = Organization(
            id=id,
            brand_name=result[0]["data"]["name"]["full_with_opf"],
            short_name=result[0]["data"]["name"]["short_with_opf"],
            inn=inn,
            okpo=result[0]["data"]["okpo"],
            ogrn=result[0]["data"]["ogrn"],
            kpp=result[0]["data"]["kpp"],
            tax_code=result[0]["data"]["address"]["data"]["tax_office"],
            address=result[0]["data"]["address"]["unrestricted_value"],
        )

        return org

    def save_docs(self, links: List[str], org_id: str) -> Optional[Exception]:
        for link in links:
            document = Document(
                id=f"doc_{uuid.uuid4()}",
                url=link,
                organization_id=org_id,
            )
            err = self.org_repository.save_docs(document)
            if err is not None:
                return err
        return None