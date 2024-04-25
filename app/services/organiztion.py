import datetime
import hashlib

from config import get_config
from dadata import Dadata
from fastapi import Depends, status
from repositories.postgres import OrganizationRepository
from repositories.postgres.schemas import Organization
from schemas import models
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

        email = result[0]["data"]["emails"]
        phone = result[0]["data"]["phones"]

        org = Organization(
            id=id,
            brand_name=result[0]["data"]["name"]["short"],
            full_name=result[0]["data"]["name"]["full_with_opf"],
            short_name=result[0]["data"]["name"]["short_with_opf"],
            inn=inn,
            okpo=result[0]["data"]["okpo"],
            ogrn=result[0]["data"]["ogrn"],
            kpp=result[0]["data"]["kpp"],
            tax_code=int(result[0]["data"]["address"]["data"]["tax_office"]),
            address=result[0]["data"]["address"]["unrestricted_value"],
            email=email[0]["source"] if email else "not found",
            phone=phone[0]["source"] if phone else "not found",
        )

        return org

    async def get_organization_by_id(self, org_id: str) -> Organization:
        org = await self.org_repository.get_organization_by_id(org_id=org_id)
        if org.update_at < datetime.datetime.now() + datetime.timedelta(
            days=30
        ):
            upd_org = self.get_organization_from_api(org.inn)
            org = await self.org_repository.update_org(upd_org=upd_org)

        return org

    async def get_organization_by_user_id(
        self, user_id: str
    ) -> models.Organization:
        org = await self.org_repository.get_organization_by_user_id(
            user_id=user_id
        )

        return org
