import hashlib
import uuid
from typing import List

from config import get_config
from dadata import Dadata
from fastapi import Depends, status
from repositories import OrganizationRepository
from repositories.schemas import Document, Organization
from services.exceptions import ServiceException


class OrganizationService:
    org_repository: OrganizationRepository

    def __init__(
        self, org_repository: OrganizationRepository = Depends()
    ) -> None:
        self.org_repository = org_repository
        self.dadata = Dadata(get_config().Dadata.api_key)

    def get_organization_from_api(self, inn: str) -> Organization:

        result = self.dadata.find_by_id("party", inn)

        if len(result) == 0:
            raise ServiceException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="INN NOT FOUND",
            )
        hash = hashlib.md5(result[0]["data"]["name"]["full_with_opf"].encode())
        id = "org_" + hash.hexdigest()

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

    def save_docs(self, links: List[str], org_id: str) -> None:
        for link in links:
            document = Document(
                id=f"doc_{uuid.uuid4()}",
                url=link,
                organization_id=org_id,
            )
            self.org_repository.save_docs(document)
