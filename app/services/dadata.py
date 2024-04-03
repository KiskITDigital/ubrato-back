from typing import List

from config import get_config
from dadata import Dadata


class DadataService:

    def __init__(self) -> None:
        self.dadata = Dadata(get_config().Dadata.api_key)

    def search_city(self, search: str) -> List[str]:
        response = self.dadata.suggest("address", search, count=20)

        result = {}
        for city in response:
            if city["data"]["city"]:
                result[city["data"]["city"]] = True

        return list(result.keys())
