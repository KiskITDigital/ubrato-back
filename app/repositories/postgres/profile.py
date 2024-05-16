from typing import Any, List

from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import (
    CV_NOT_FOUND,
    PROFILE_NOT_FOUND,
    RepositoryException,
)
from repositories.postgres.schemas import (
    City,
    ContractorCV,
    ContractorLocation,
    ContractorObject,
    ContractorProfile,
    ContractorService,
    CustomerLocation,
    CustomerProfile,
    ServiceType,
)
from schemas import models
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class ProfileRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def get_customer(self, org_id: str) -> CustomerProfile:
        query = await self.db.execute(
            select(CustomerProfile).where(CustomerProfile.org_id == org_id)
        )

        profile = query.scalar()
        if profile is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=PROFILE_NOT_FOUND.format(org_id),
                sql_msg="",
            )

        return profile

    async def get_customer_location(self, org_id: str) -> List[str]:
        query = await self.db.execute(
            select(City.name)
            .select_from(CustomerLocation)
            .join(City)
            .where(
                and_(
                    City.id == CustomerLocation.city_id,
                    CustomerLocation.org_id == org_id,
                )
            )
        )

        locations: List[str] = []
        for location in query.scalars().all():
            locations.append(location)

        return locations

    async def get_contractor(self, org_id: str) -> ContractorProfile:
        query = await self.db.execute(
            select(ContractorProfile).where(ContractorProfile.org_id == org_id)
        )

        profile = query.scalar()
        if profile is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=PROFILE_NOT_FOUND.format(org_id),
                sql_msg="",
            )

        return profile

    async def get_contractor_location(self, org_id: str) -> List[str]:
        query = await self.db.execute(
            select(City.name)
            .select_from(ContractorLocation)
            .join(City)
            .where(
                and_(
                    City.id == ContractorLocation.city_id,
                    ContractorLocation.org_id == org_id,
                )
            )
        )

        locations: List[str] = []
        for location in query.scalars().all():
            locations.append(location)

        return locations

    async def get_contractor_services_pricing(
        self, org_id: str
    ) -> List[models.ContractorPricing]:
        query = await self.db.execute(
            select(ContractorService.price, ServiceType.name)
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
            price, name = service._tuple()
            services.append(
                models.ContractorPricing(
                    name=name,
                    price=price,
                )
            )

        return services

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
                detail=CV_NOT_FOUND.format(cv_id),
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
                detail=CV_NOT_FOUND.format(cv_id),
                sql_msg="",
            )

        for key, value in cv.items():
            setattr(cv_to_update, key, value)

        await self.db.commit()

    async def delete_contractor_cv(self, cv_id: str) -> None:
        await self.db.execute(
            delete(ContractorCV).where(ContractorCV.id == cv_id)
        )

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
                detail=PROFILE_NOT_FOUND.format(org_id),
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
                detail=PROFILE_NOT_FOUND.format(org_id),
                sql_msg="",
            )

        profile_to_update.description = description

        await self.db.commit()
