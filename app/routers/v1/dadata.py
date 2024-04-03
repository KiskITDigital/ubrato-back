from fastapi import APIRouter, Depends
from schemas.suggest import SuggestRespone
from services import DadataService

router = APIRouter(
    prefix="/v1/dadata",
    tags=["dadata"],
)


@router.get(
    "/suggest/city",
    response_model=SuggestRespone,
)
async def search_city(
    query: str,
    dadata_service: DadataService = Depends(),
) -> SuggestRespone:
    return SuggestRespone(suggestions=dadata_service.search_city(query))
