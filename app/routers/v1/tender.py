from typing import List, Optional

import models
from fastapi import APIRouter, Depends, status
from models import ObjectsGroupsWithTypes, ServicesGroupsWithTypes
from routers.v1.dependencies import authorized, get_user, is_creator_or_manager
from schemas.create_tender import CreateTenderRequest
from schemas.exception import ExceptionResponse, UnauthExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.success import SuccessResponse
from schemas.tender_count import TenderCountResponse
from services import TenderService

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
    created_tender = tender_service.create_tender(
        tender=tender, user_id=user.id
    )
    return created_tender


@router.get(
    "/",
    response_model=List[models.Tender],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
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

    tenders = tender_service.get_page_tenders(
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
    tender = tender_service.get_by_id(tender_id=tender_id)
    return tender


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
    original_tender = tender_service.get_by_id(tender_id=tender_id)

    await is_creator_or_manager(user_id=original_tender.user_id, user=user)

    tender_service.update_tender(tender=tender, tender_id=tender_id)
    return SuccessResponse()


@router.get(
    "/objects-types",
    response_model=ObjectsGroupsWithTypes,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def get_all_objects_types(
    tender_service: TenderService = Depends(),
) -> ObjectsGroupsWithTypes:
    objects = tender_service.get_all_objects_with_types()
    return objects


@router.get(
    "/services-types",
    response_model=ServicesGroupsWithTypes,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def get_all_services_types(
    tender_service: TenderService = Depends(),
) -> ServicesGroupsWithTypes:
    objects = tender_service.get_all_services_with_types()
    return objects


@router.get(
    "/stats/count",
    response_model=TenderCountResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def get_count_active_tenders(
    object_group_id: Optional[int] = None,
    service_type_id: Optional[int] = None,
    tender_service: TenderService = Depends(),
) -> TenderCountResponse:
    count = tender_service.get_count_active_tenders(
        object_group_id=object_group_id, service_type_id=service_type_id
    )

    return TenderCountResponse(count=count)
