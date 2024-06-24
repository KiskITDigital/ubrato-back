from typing import List

from config import get_config
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import RepositoryException
from repositories.postgres.schemas import City, Region
from schemas import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CitiesRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db
        self.localization = get_config().Localization.config

    async def get_by_id(self, city_id: int) -> City:
        query = await self.db.execute(select(City).where(City.id == city_id))

        city = query.scalar()

        if city is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.localization["errors"]["city_not_fount"].format(
                    city_id
                ),
                sql_msg="",
            )
        return city

    async def search_by_name(self, name: str) -> List[models.City]:
        query = await self.db.execute(
            select(City, Region.name)
            .join(Region, City.region_id == Region.id)
            .where(City.name.ilike(name + "%"))
            .limit(10)
        )

        cities: List[models.City] = []
        for found_city in query.all():
            city, region_name = found_city._tuple()
            city_model = models.City(
                id=city.id,
                name=city.name,
                region=region_name,
            )
            cities.append(city_model)

        return cities
