from typing import List
from exceptions import ServiceException
from fastapi import APIRouter, Depends, status
from models import tender_model
from models.object_group import ObjectsGroupsWithTypes
from models.service_group import ServicesGroupsWithTypes
from routers.v1.dependencies import authorized, get_user
from schemas.create_tender import CreateTenderRequest, CreateTenderResponse
from schemas.exception import ExceptionResponse, UnauthExceptionResponse
from schemas.jwt_user import JWTUser
from services.logs import LogsService
from services.tenders import TenderService

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
    response_model=List[tender_model.Tender],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def get_page_tenders(
    page: int = 1,
    page_size: int = 10,
    tender_service: TenderService = Depends(),
    logs_service: LogsService = Depends(),
) -> ObjectsGroupsWithTypes:
    tenders, err = tender_service.get_page_active_tenders(page=page, page_size=page_size)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
    return tenders


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
