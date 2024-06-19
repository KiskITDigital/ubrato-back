from typing import Any, List, Tuple

from config import get_config
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import RepositoryException
from repositories.postgres.schemas import (
    City,
    ContractorCV,
    ContractorLocation,
    ContractorObject,
    ContractorProfile,
    ContractorService,
    CustomerLocation,
    CustomerProfile,
    ObjectType,
    Organization,
    ServiceType,
)
from schemas import models
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ProfileRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def set_brand_avatar(self, org_id: str, url: str) -> None:
        query = await self.db.execute(
            select(Organization).where(Organization.id == org_id)
        )

        org = query.scalar()

        if org is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["org_not_found"]
                .format(org_id),
                sql_msg="",
            )

        org.avatar = url
        await self.db.commit()

    async def set_brand_name(self, org_id: str, name: str) -> None:
        stmn = (
            update(Organization)
            .where(Organization.id == org_id)
            .values(brand_name=name)
        )
        await self.db.execute(stmn)

    async def get_customer(self, org_id: str) -> CustomerProfile:
        query = await self.db.execute(
            select(CustomerProfile).where(CustomerProfile.org_id == org_id)
        )

        profile = query.scalar()
        if profile is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["profile_not_found"]
                .format(org_id),
                sql_msg="",
            )

        return profile

    async def get_customer_location(
        self, org_id: str
    ) -> List[models.ProfileLocation]:
        query = await self.db.execute(
            select(City.id, City.name)
            .select_from(CustomerLocation)
            .join(City)
            .where(
                and_(
                    City.id == CustomerLocation.city_id,
                    CustomerLocation.org_id == org_id,
                )
            )
        )

        locations: List[models.ProfileLocation] = []
        for location in query.all():
            id, name = location.tuple()
            locations.append(models.ProfileLocation(id=id, name=name))

        return locations

    async def get_contractor(self, org_id: str) -> ContractorProfile:
        query = await self.db.execute(
            select(ContractorProfile).where(ContractorProfile.org_id == org_id)
        )

        profile = query.scalar()
        if profile is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["profile_not_found"]
                .format(org_id),
                sql_msg="",
            )

        return profile

    async def get_contractor_location(
        self, org_id: str
    ) -> List[models.ProfileLocation]:
        query = await self.db.execute(
            select(City.id, City.name)
            .select_from(ContractorLocation)
            .join(City)
            .where(
                and_(
                    City.id == ContractorLocation.city_id,
                    ContractorLocation.org_id == org_id,
                )
            )
        )

        locations: List[models.ProfileLocation] = []
        for location in query.all():
            id, name = location.tuple()
            locations.append(models.ProfileLocation(id=id, name=name))

        return locations

    async def get_contractor_services_pricing(
        self, org_id: str
    ) -> List[models.ContractorPricing]:
        query = await self.db.execute(
            select(ContractorService.price, ServiceType.id, ServiceType.name)
            .join(
                ServiceType,
                ServiceType.id == ContractorService.service_type_id,
            )
            .where(
                ContractorService.org_id == org_id,
            )
        )

        services: List[models.ContractorPricing] = []
        for service in query.all():
            price, id, name = service._tuple()
            services.append(
                models.ContractorPricing(
                    id=id,
                    name=name,
                    price=price,
                )
            )

        return services

    async def get_contractor_objects(
        self, org_id: str
    ) -> List[models.ContractorObject]:
        query = await self.db.execute(
            select(ObjectType.id, ObjectType.name)
            .join(
                ContractorObject,
                ObjectType.id == ContractorObject.object_type_id,
            )
            .where(
                ContractorObject.org_id == org_id,
            )
        )

        objects: List[models.ContractorObject] = []
        for service in query.all():
            id, name = service._tuple()
            objects.append(
                models.ContractorObject(
                    id=id,
                    name=name,
                )
            )

        return objects

    async def get_contractor_cv(
        self, org_id: str
    ) -> List[models.ContractorCV]:
        query = await self.db.execute(
            select(ContractorCV).where(ContractorCV.org_id == org_id)
        )

        cv: List[models.ContractorCV] = []
        for work in query.scalars().all():
            cv.append(
                models.ContractorCV(
                    id=work.id,
                    name=work.name,
                    description=work.description,
                    links=work.links,
                )
            )

        return cv

    async def get_contractor_cv_by_id(self, cv_id: str) -> ContractorCV:
        query = await self.db.execute(
            select(ContractorCV).where(ContractorCV.id == cv_id)
        )

        cv = query.scalar()
        if cv is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["cv_not_found"]
                .format(cv_id),
                sql_msg="",
            )

        return cv

    async def set_contractor_services(
        self, org_id: str, services: List[ContractorService]
    ) -> None:
        await self.db.execute(
            delete(ContractorService).where(ContractorService.org_id == org_id)
        )
        self.db.add_all(services)

        await self.db.commit()

    async def set_contractor_objects(
        self, org_id: str, objects: List[ContractorObject]
    ) -> None:
        await self.db.execute(
            delete(ContractorObject).where(ContractorObject.org_id == org_id)
        )
        self.db.add_all(objects)

        await self.db.commit()

    async def save_contractor_cv(self, cv: ContractorCV) -> str:
        self.db.add(cv)
        await self.db.commit()
        await self.db.refresh(cv)
        return cv.id

    async def update_contractor_cv(
        self, cv: dict[str, Any], cv_id: str
    ) -> None:
        query = await self.db.execute(
            select(ContractorCV).where(ContractorCV.id == cv_id)
        )

        cv_to_update = query.scalar()
        if cv_to_update is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["cv_not_found"]
                .format(cv_id),
                sql_msg="",
            )

        for key, value in cv.items():
            setattr(cv_to_update, key, value)

        await self.db.commit()

    async def delete_contractor_cv(self, cv_id: str) -> None:
        await self.db.execute(
            delete(ContractorCV).where(ContractorCV.id == cv_id)
        )

        await self.db.commit()

    async def set_contractor_locations(
        self, org_id: str, locations: List[ContractorLocation]
    ) -> None:
        await self.db.execute(
            delete(ContractorLocation).where(
                ContractorLocation.org_id == org_id
            )
        )
        self.db.add_all(locations)
        await self.db.commit()

    async def set_customer_location(
        self, org_id: str, locations: List[CustomerLocation]
    ) -> None:
        await self.db.execute(
            delete(CustomerLocation).where(CustomerLocation.org_id == org_id)
        )
        self.db.add_all(locations)
        await self.db.commit()

    async def update_contractor_info(
        self, org_id: str, description: str
    ) -> None:
        query = await self.db.execute(
            select(ContractorProfile).where(ContractorProfile.org_id == org_id)
        )

        profile_to_update = query.scalar()
        if profile_to_update is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["profile_not_found"]
                .format(org_id),
                sql_msg="",
            )

        profile_to_update.description = description

        await self.db.commit()

    async def update_customer_info(
        self, org_id: str, description: str
    ) -> None:
        query = await self.db.execute(
            select(CustomerProfile).where(CustomerProfile.org_id == org_id)
        )

        profile_to_update = query.scalar()
        if profile_to_update is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["profile_not_found"]
                .format(org_id),
                sql_msg="",
            )

        profile_to_update.description = description

        await self.db.commit()

    async def set_brand_emails(
        self, org_id: str, emails: List[Tuple[str, str]]
    ) -> None:
        await self.db.execute(
            update(Organization)
            .values(
                email=[
                    {"contact": contact, "description": description}
                    for contact, description in emails
                ]
            )
            .where(Organization.id == org_id)
        )
        await self.db.commit()

    async def set_brand_phones(
        self, org_id: str, phones: List[Tuple[str, str]]
    ) -> None:
        await self.db.execute(
            update(Organization)
            .values(
                phone=[
                    {"contact": contact, "description": description}
                    for contact, description in phones
                ]
            )
            .where(Organization.id == org_id)
        )
        await self.db.commit()

    async def set_brand_messengers(
        self, org_id: str, messengers: List[Tuple[str, str]]
    ) -> None:
        await self.db.execute(
            update(Organization)
            .values(
                messenger=[
                    {"contact": contact, "description": description}
                    for contact, description in messengers
                ]
            )
            .where(Organization.id == org_id)
        )
        await self.db.commit()
