from typing import List

from fastapi import Depends
from repositories.postgres import CitiesRepository
from schemas import models
from tools.egrul import get_org_by_query


class SuggestService:
    cities_repository: CitiesRepository

    def __init__(
        self,
        cities_repository: CitiesRepository = Depends(),
    ) -> None:
        self.cities_repository = cities_repository

    async def search_city(self, query: str) -> List[models.City]:
        return await self.cities_repository.search_by_name(name=query)

    async def search_company(self, query: str) -> List[models.EgrulCompany]:
        return get_org_by_query(query=query)
