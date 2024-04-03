from typing import List, Tuple

from fastapi import Depends
from repositories import CitiesRepository


class SuggestService:
    cities_repository: CitiesRepository

    def __init__(
        self,
        cities_repository: CitiesRepository = Depends(),
    ) -> None:
        self.cities_repository = cities_repository

    def search_city(self, query: str) -> List[Tuple[str, str]]:
        return self.cities_repository.search_by_name(name=query)
