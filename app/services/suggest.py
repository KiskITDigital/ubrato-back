from typing import List

from fastapi import Depends
from repositories.postgres import CitiesRepository
from schemas import models


class SuggestService:
    cities_repository: CitiesRepository

    def __init__(
        self,
        cities_repository: CitiesRepository = Depends(),
    ) -> None:
        self.cities_repository = cities_repository

    async def search_city(self, query: str) -> List[models.City]:
        return await self.cities_repository.search_by_name(name=query)
