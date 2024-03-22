from typing import List, Optional

import models
from exceptions import ServiceException
from fastapi import APIRouter, Depends, status
from models import ObjectsGroupsWithTypes, ServicesGroupsWithTypes
from routers.v1.dependencies import authorized, get_user, is_creator_or_manager
from routers.v1.exceptions import TENDER_NOT_FOUND
from schemas.create_tender import CreateTenderRequest, CreateTenderResponse
from schemas.exception import ExceptionResponse, UnauthExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.success import SuccessResponse
from schemas.tender_count import TenderCountResponse
from services import LogsService, TenderService

router = APIRouter(
    prefix="/v1/tenders",
    tags=["tenders"],
)


@router.post(
    "/create",
    response_model=CreateTenderResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def create_tender(
    tender: CreateTenderRequest,
    tender_service: TenderService = Depends(),
    logs_service: LogsService = Depends(),
    user: JWTUser = Depends(get_user),
) -> CreateTenderResponse:
    id, err = tender_service.create_tender(tender=tender, user_id=user.id)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
    return CreateTenderResponse(id=id)


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
    service_type_ids: Optional[List[int]] = None,
    service_group_ids: Optional[List[int]] = None,
    floor_space_from: Optional[int] = None,
    floor_space_to: Optional[int] = None,
    price_from: Optional[int] = None,
    price_to: Optional[int] = None,
    text: Optional[str] = None,
    active: Optional[bool] = True,
    verified: Optional[bool] = True,
    user_id: Optional[str] = None,
    tender_service: TenderService = Depends(),
    logs_service: LogsService = Depends(),
) -> ObjectsGroupsWithTypes:
    tenders, err = tender_service.get_page_tenders(
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
        text=text,
        active=active,
        verified=verified,
        user_id=user_id,
    )
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
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
    tender_id: str,
    tender_service: TenderService = Depends(),
    logs_service: LogsService = Depends(),
) -> models.Tender:
    tender, err = tender_service.get_by_id(id=tender_id)
    if tender is None:
        raise ServiceException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TENDER_NOT_FOUND,
            logs_service=logs_service,
        )
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
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
    tender_id: str,
    tender: CreateTenderRequest,
    tender_service: TenderService = Depends(),
    logs_service: LogsService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    original_tender, err = tender_service.get_by_id(id=tender_id)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
    if tender is None:
        raise ServiceException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TENDER_NOT_FOUND,
            logs_service=logs_service,
        )

    await is_creator_or_manager(user_id=original_tender.user_id, user=user)
    err = tender_service.update_tender(tender=tender, tender_id=tender_id)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
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
    logs_service: LogsService = Depends(),
) -> ObjectsGroupsWithTypes:
    objects, err = tender_service.get_all_objects_with_types()
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
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
    logs_service: LogsService = Depends(),
) -> ServicesGroupsWithTypes:
    objects, err = tender_service.get_all_services_with_types()
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
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
    logs_service: LogsService = Depends(),
) -> ServicesGroupsWithTypes:
    count, err = tender_service.get_count_active_tenders(
        object_group_id=object_group_id, service_type_id=service_type_id
    )
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )

    return TenderCountResponse(count=count)
