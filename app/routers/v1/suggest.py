from fastapi import APIRouter, Depends
from schemas.suggest import SuggestRespone
from services import SuggestService

router = APIRouter(
    prefix="/v1/suggest",
    tags=["dadata"],
)


@router.get(
    "/city",
    response_model=SuggestRespone,
)
async def search_city(
    query: str,
    suggest_service: SuggestService = Depends(),
) -> SuggestRespone:
    return SuggestRespone(suggestions=suggest_service.search_city(query=query))
