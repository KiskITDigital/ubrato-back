from typing import List

import models
from fastapi import APIRouter, Depends
from services import SuggestService

router = APIRouter(
    prefix="/v1/suggest",
    tags=["suggest"],
)


@router.get(
    "/city",
    response_model=List[models.City],
)
async def search_city(
    query: str,
    suggest_service: SuggestService = Depends(),
) -> List[models.City]:
    return suggest_service.search_city(query=query)
