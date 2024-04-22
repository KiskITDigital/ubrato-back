from typing import List

from fastapi import APIRouter, Depends
from schemas import models
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
    return await suggest_service.search_city(query=query)


@router.get(
    "/company",
    response_model=List[models.EgrulCompany],
)
async def search_company(
    query: str,
    suggest_service: SuggestService = Depends(),
) -> List[models.EgrulCompany]:
    return await suggest_service.search_company(query=query)
