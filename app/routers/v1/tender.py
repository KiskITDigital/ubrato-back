from typing import List, Optional

from fastapi import APIRouter, Depends, status
from routers.v1.dependencies import (
    authorized,
    get_user,
    is_creator_or_manager,
    localization,
)
from schemas import models
from schemas.create_draft_tender import CreateDraftTenderRequest
from schemas.create_tender import CreateTenderRequest
from schemas.exception import ExceptionResponse, UnauthExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.models import ObjectsGroupsWithTypes, ServicesGroupsWithTypes
from schemas.success import SuccessResponse
from schemas.tender_count import TenderCountResponse
from schemas.tender_respond import TenderRespondRequest
from services import DraftTenderService, TenderService
from services.exceptions import ServiceException
from tools.cache import redis_cache

router = APIRouter(
    prefix="/v1/tenders",
    tags=["tenders"],
)


@router.post(
    "/create",
    response_model=models.Tender,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def create_tender(
    tender: CreateTenderRequest,
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> models.Tender:
    created_tender = await tender_service.create_tender(
        tender=tender, user_id=user.id
    )
    return created_tender


@router.get(
    "/",
    response_model=List[models.Tender],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    deprecated=True,
    description="Migrate to: https://search.ubrato.ru | https://typesense.org/docs/",
)
async def get_page_tenders(
    page: int = 1,
    page_size: int = 10,
    object_group_id: Optional[int] = None,
    object_type_id: Optional[int] = None,
    service_type_ids_str: Optional[str] = None,
    service_group_ids_str: Optional[str] = None,
    floor_space_from: Optional[int] = None,
    floor_space_to: Optional[int] = None,
    price_from: Optional[int] = None,
    price_to: Optional[int] = None,
    verified: Optional[bool] = True,
    user_id: Optional[str] = None,
    tender_service: TenderService = Depends(),
) -> List[models.Tender]:
    service_type_ids: List[int] | None = None
    if service_type_ids_str is not None:
        service_type_ids = [int(x) for x in service_type_ids_str.split(",")]

    service_group_ids: List[int] | None = None
    if service_group_ids_str is not None:
        service_group_ids = [int(x) for x in service_group_ids_str.split(",")]

    tenders = await tender_service.get_page_tenders(
        page=page,
        page_size=page_size,
        object_group_id=object_group_id,
        object_type_id=object_type_id,
        service_type_ids=service_type_ids,
        service_group_ids=service_group_ids,
        floor_space_from=floor_space_from,
        floor_space_to=floor_space_to,
        price_from=price_from,
        price_to=price_to,
        verified=verified,
        user_id=user_id,
    )
    return tenders


@router.get(
    "/tender/{tender_id}",
    response_model=models.Tender,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
)
async def get_tender(
    tender_id: int,
    tender_service: TenderService = Depends(),
) -> models.Tender:
    tender = await tender_service.get_by_id(tender_id=tender_id)
    return tender


@router.post(
    "/tender/{tender_id}/respond",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def respond_tender(
    tender_id: int,
    data: TenderRespondRequest,
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await tender_service.respond_tender(
        tender_id=tender_id, user_id=user.id, price=data.price
    )
    return SuccessResponse()


@router.get(
    "/tender/{tender_id}/is_respond",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_tender_respond_status(
    tender_id: int,
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    return SuccessResponse(
        status=await tender_service.is_responded(
            tender_id=tender_id, user_id=user.id
        )
    )


@router.get(
    "/tender/{tender_id}/has_offer/{org_id}",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def is_has_offer(
    tender_id: int,
    org_id: str,
    tender_service: TenderService = Depends(),
) -> SuccessResponse:
    return SuccessResponse(
        status=await tender_service.is_has_offer(
            tender_id=tender_id, org_id=org_id
        )
    )


@router.put(
    "/tender/{tender_id}",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def update_tender(
    tender_id: int,
    tender: CreateTenderRequest,
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    original_tender = await tender_service.get_by_id(tender_id=tender_id)

    await is_creator_or_manager(user_id=original_tender.user_id, user=user)

    await tender_service.update_tender(tender=tender, tender_id=tender_id)
    return SuccessResponse()


@router.get(
    "/objects-types",
    response_model=ObjectsGroupsWithTypes,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
@redis_cache(ignore_classes=[TenderService])
async def get_all_objects_types(
    tender_service: TenderService = Depends(),
) -> ObjectsGroupsWithTypes:
    objects = await tender_service.get_all_objects_with_types()
    return objects


@router.get(
    "/services-types",
    response_model=ServicesGroupsWithTypes,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
@redis_cache(ignore_classes=[TenderService])
async def get_all_services_types(
    tender_service: TenderService = Depends(),
) -> ServicesGroupsWithTypes:
    objects = await tender_service.get_all_services_with_types()
    return objects


@router.get(
    "/stats/count",
    response_model=TenderCountResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def get_count_active_tenders(
    object_type_id: Optional[int] = None,
    service_type_id: Optional[int] = None,
    tender_service: TenderService = Depends(),
) -> TenderCountResponse:
    count = await tender_service.get_count_active_tenders(
        object_type_id=object_type_id, service_type_id=service_type_id
    )

    return TenderCountResponse(count=count)


@router.post(
    "/draft",
    response_model=models.DraftTender,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
    },
    dependencies=[Depends(authorized)],
    tags=["draft"],
)
async def create_draft_tender(
    tender: CreateDraftTenderRequest,
    tender_service: DraftTenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> models.DraftTender:
    created_tender = await tender_service.create_tender(
        tender=tender, user_id=user.id
    )
    return created_tender


@router.put(
    "/draft/{id}",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
    tags=["draft"],
)
async def update_draft_tender(
    id: int,
    new_tender: CreateDraftTenderRequest,
    tender_service: DraftTenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    tender = await tender_service.get_by_id(id=id)
    if tender.user_id != user.id:
        raise ServiceException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=localization["errors"]["no_access"],
        )
    await tender_service.update_tender(tender=new_tender, id=id)
    return SuccessResponse()


@router.delete(
    "/draft/{id}",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
    tags=["draft"],
)
async def delete_draft_tender(
    id: int,
    tender_service: DraftTenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    tender = await tender_service.get_by_id(id=id)
    if tender.user_id != user.id:
        raise ServiceException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=localization["errors"]["no_access"],
        )
    await tender_service.delete_tender(id=id)
    return SuccessResponse()


@router.get(
    "/draft/{id}",
    response_model=models.DraftTender,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
    tags=["draft"],
)
async def get_draft_tender(
    id: int,
    tender_service: DraftTenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> models.DraftTender:
    tender = await tender_service.get_by_id(id=id)
    if tender.user_id != user.id:
        raise ServiceException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=localization["errors"]["no_access"],
        )
    return await tender_service.get_by_id(id=id)


@router.get(
    "/tender/{tender_id}/is_favorite",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def is_favorite(
    tender_id: int,
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    return SuccessResponse(
        status=await tender_service.is_favorite(
            tender_id=tender_id, user_id=user.id
        )
    )


@router.post(
    "/tender/{tender_id}/favorite",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def add_favorite(
    tender_id: int,
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await tender_service.add_to_favorite(tender_id=tender_id, user_id=user.id)
    return SuccessResponse()


@router.delete(
    "/tender/{tender_id}/favorite",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def remove_favorite(
    tender_id: int,
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await tender_service.remove_from_favorite(
        tender_id=tender_id, user_id=user.id
    )
    return SuccessResponse()


@router.get(
    "/my/drafts",
    response_model=List[models.DraftTender],
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
    tags=["draft"],
)
async def get_user_drafts(
    tender_service: DraftTenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> List[models.DraftTender]:
    return await tender_service.get_user_tenders(user_id=user.id)


@router.get(
    "/my/tenders",
    response_model=List[models.Tender],
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_user_tenders(
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> List[models.Tender]:
    return await tender_service.get_user_tenders(user_id=user.id)


@router.get(
    "/my/tenders/{tender_id}/responses",
    response_model=List[models.TenderResponse],
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_tender_responses(
    tender_id: int,
    tender_service: TenderService = Depends(),
    user: JWTUser = Depends(get_user),
) -> List[models.TenderResponse]:
    return await tender_service.get_tender_responses(tender_id=tender_id)
