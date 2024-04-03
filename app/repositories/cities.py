from typing import List, Tuple

from fastapi import Depends, status
from repositories.database import get_db_connection
from repositories.exceptions import CITY_NOT_FOUNT, RepositoryException
from repositories.schemas import City, Region
from sqlalchemy.orm import Session, scoped_session


class CitiesRepository:
    db: scoped_session[Session]

    def __init__(
        self, db: scoped_session[Session] = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def get_by_id(self, city_id: int) -> City:
        city = self.db.query(City).filter_by(id=city_id).first()

        if city is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CITY_NOT_FOUNT.format(city_id),
                sql_msg="",
            )
        return city

    def search_by_name(self, name: str) -> List[Tuple[str, str]]:
        results = (
            self.db.query(City, Region.name)
            .join(Region, City.region_id == Region.id)
            .filter(City.name.ilike(name + "%"))
            .limit(10)
        )
        return [(city.name, region_name) for city, region_name in results]
