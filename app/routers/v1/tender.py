from fastapi import APIRouter, Depends, status
from exceptions import ServiceException
from models.object_group import ObjectsGroupsWithTypes
from models.service_group import ServicesGroupsWithTypes

from services.logs import LogsService
from services.tenders import TenderService

router = APIRouter(
    prefix="/v1/tenders",
    tags=["tenders"],
)

@router.get(
    "/objects-types",
    response_model=ObjectsGroupsWithTypes,
)
async def get_all_objects_types(
    tender_service: TenderService = Depends(),
    logs_service: LogsService = Depends(),
):
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
)
async def get_all_services_types(
    tender_service: TenderService = Depends(),
    logs_service: LogsService = Depends(),
):
    objects, err = tender_service.get_all_services_with_types()
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
    return objects