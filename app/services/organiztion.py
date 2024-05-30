import datetime
import hashlib
import uuid
from typing import Any, Dict, List, Tuple

from config import get_config
from dadata import Dadata
from fastapi import Depends, status
from repositories.postgres import OrganizationRepository, ProfileRepository
from repositories.postgres.schemas import (
    ContractorCV,
    ContractorLocation,
    ContractorObject,
    ContractorService,
    CustomerLocation,
    Organization,
)
from repositories.typesense import ContractorIndex
from repositories.typesense.schemas import TypesenseContractorService
from schemas import models
from services.exceptions import ServiceException


class OrganizationService:
    org_repository: OrganizationRepository
    profile_repository: ProfileRepository
    contractor_index: ContractorIndex

    def __init__(
        self,
        org_repository: OrganizationRepository = Depends(),
        profile_repository: ProfileRepository = Depends(),
        contractor_index: ContractorIndex = Depends(),
    ) -> None:
        self.org_repository = org_repository
        self.profile_repository = profile_repository
        self.contractor_index = contractor_index
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
            org.update_at + datetime.timedelta(days=30)
            < datetime.datetime.now().astimezone()
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
            await self.profile_repository.get_contractor_location(
                org_id=org_id
            )
        )

        contractor_pricing = (
            await self.profile_repository.get_contractor_services_pricing(
                org_id=org_id
            )
        )

        contractor_objects = (
            await self.profile_repository.get_contractor_objects(org_id=org_id)
        )

        contractor_cv = await self.profile_repository.get_contractor_cv(
            org_id=org_id
        )

        return models.ContractorProfile(
            description=contractor_info.description,
            locations=contractor_locations,
            services=contractor_pricing,
            objects=contractor_objects,
            portfolio=contractor_cv,
        )

    async def update_customer_info(
        self, org_id: str, description: str
    ) -> None:
        await self.profile_repository.update_customer_info(
            org_id=org_id, description=description
        )

    async def set_customer_locations(
        self, org_id: str, locations: List[CustomerLocation]
    ) -> None:
        await self.profile_repository.set_customer_location(
            org_id=org_id, locations=locations
        )

    async def update_contractor_info(
        self, org_id: str, description: str
    ) -> None:
        await self.profile_repository.update_contractor_info(
            org_id=org_id, description=description
        )

    async def set_contractor_locations(
        self, org_id: str, locations: List[ContractorLocation]
    ) -> None:
        self.contractor_index.update_locations(
            contractor_id=org_id, locations=[id.city_id for id in locations]
        )
        await self.profile_repository.set_contractor_locations(
            org_id=org_id, locations=locations
        )

    async def set_contractor_services(
        self, org_id: str, services: List[ContractorService]
    ) -> None:
        self.contractor_index.update_services(
            contractor_id=org_id,
            services=[
                TypesenseContractorService(
                    contractor_id=org_id,
                    service_type_id=str(service.service_type_id),
                    price=service.price,
                )
                for service in services
            ],
        )

        await self.profile_repository.set_contractor_services(
            org_id=org_id, services=services
        )

    async def set_contractor_objects(
        self, org_id: str, objects: List[ContractorObject]
    ) -> None:
        self.contractor_index.update_objects(
            contractor_id=org_id,
            objects=[object.object_type_id for object in objects],
        )

        await self.profile_repository.set_contractor_objects(
            org_id=org_id, objects=objects
        )

    async def save_contractor_cv(
        self, org_id: str, name: str, description: str, links: List[str]
    ) -> str:
        id = "cv_" + str(uuid.uuid4())
        cv: ContractorCV = ContractorCV(
            id=id,
            org_id=org_id,
            name=name,
            description=description,
            links=links,
        )
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

    async def set_brand_avatar(self, org_id: str, url: str) -> None:
        await self.profile_repository.set_brand_avatar(org_id=org_id, url=url)

    async def set_brand_name(self, org_id: str, name: str) -> None:
        await self.profile_repository.set_brand_name(org_id=org_id, name=name)

    async def set_brand_contact_info(
        self,
        org_id: str,
        emails: List[Tuple[str, str]],
        phones: List[Tuple[str, str]],
        messengers: List[Tuple[str, str]],
    ) -> None:
        await self.profile_repository.set_brand_emails(
            org_id=org_id, emails=emails
        )
        await self.profile_repository.set_brand_phones(
            org_id=org_id, phones=phones
        )
        await self.profile_repository.set_brand_messengers(
            org_id=org_id, messengers=messengers
        )
