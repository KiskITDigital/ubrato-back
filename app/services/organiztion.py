import datetime
import hashlib
import uuid
from typing import Any, Dict, List

from config import get_config
from dadata import Dadata
from fastapi import Depends, status
from repositories.postgres import OrganizationRepository, ProfileRepository
from repositories.postgres.schemas import (
    ContractorCV,
    ContractorLocation,
    ContractorObject,
    ContractorService,
    Organization,
)
from schemas import models
from services.exceptions import ServiceException


class OrganizationService:
    org_repository: OrganizationRepository
    profile_repository: ProfileRepository

    def __init__(
        self,
        org_repository: OrganizationRepository = Depends(),
        profile_repository: ProfileRepository = Depends(),
    ) -> None:
        self.org_repository = org_repository
        self.profile_repository = profile_repository
        self.dadata = Dadata(get_config().Dadata.api_key)

    def get_organization_from_api(self, inn: str) -> Organization:

        result = self.dadata.find_by_id("party", inn)

        if len(result) == 0:
            raise ServiceException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="INN NOT FOUND",
            )
        hash = hashlib.md5(inn.encode())
        id = "org_" + hash.hexdigest()

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
        )

        return org

    async def get_organization_by_id(self, org_id: str) -> Organization:
        org = await self.org_repository.get_organization_by_id(org_id=org_id)
        if (
            org.update_at
            < datetime.datetime.now().astimezone()
            + datetime.timedelta(days=30)
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

    async def get_customer_profile(
        self, org_id: str
    ) -> models.CustomerProfile:
        customer_info = await self.profile_repository.get_customer(
            org_id=org_id
        )
        customer_locations = (
            await self.profile_repository.get_customer_location(org_id=org_id)
        )

        return models.CustomerProfile(
            description=customer_info.description,
            locations=customer_locations,
        )

    async def get_contractor_profile(
        self, org_id: str
    ) -> models.ContractorProfile:
        contractor_info = await self.profile_repository.get_contractor(
            org_id=org_id
        )
        contractor_locations = (
            await self.profile_repository.get_contractor_location(org_id=org_id)
        )

        contractor_pricing = (
            await self.profile_repository.get_contractor_services_pricing(
                org_id=org_id
            )
        )

        contractor_cv = await self.profile_repository.get_contractor_cv(
            org_id=org_id
        )

        return models.ContractorProfile(
            description=contractor_info.description,
            locations=contractor_locations,
            services=contractor_pricing,
            portfolio=contractor_cv,
        )

    async def set_contractor_services(
        self, org_id: str, services: List[ContractorService]
    ) -> None:
        await self.profile_repository.set_contractor_services(
            org_id=org_id, services=services
        )

    async def set_contractor_locations(
        self, org_id: str, locations: List[ContractorLocation]
    ) -> None:
        await self.profile_repository.set_contractor_locations(
            org_id=org_id, locations=locations
        )

    async def set_contractor_objects(
        self, org_id: str, objects: List[ContractorObject]
    ) -> None:
        await self.profile_repository.set_contractor_objects(
            org_id=org_id, objects=objects
        )

    async def save_contractor_cv(self, cv: ContractorCV) -> str:
        id = "cv_" + str(uuid.uuid4())
        cv.id = id
        return await self.profile_repository.save_contractor_cv(cv=cv)

    async def update_contractor_cv(
        self, cv_id: str, cv: Dict[str, Any]
    ) -> None:
        await self.profile_repository.update_contractor_cv(cv_id=cv_id, cv=cv)

    async def delete_contractor_cv(self, cv_id: str) -> None:
        await self.profile_repository.delete_contractor_cv(cv_id=cv_id)

    async def get_contractor_cv(
        self, org_id: str
    ) -> List[models.ContractorCV]:
        return await self.profile_repository.get_contractor_cv(org_id=org_id)

    async def get_contractor_cv_by_id(self, cv_id: str) -> ContractorCV:
        return await self.profile_repository.get_contractor_cv_by_id(
            cv_id=cv_id
        )
