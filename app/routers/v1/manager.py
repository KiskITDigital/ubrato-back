from typing import List

import models
from fastapi import APIRouter, Depends, status
from routers.v1.dependencies import is_admin
from schemas.exception import ExceptionResponse
from schemas.success import SuccessResponse
from schemas.verify_status_set import VerifyStatusSet
from services import ManagerService

router = APIRouter(
    prefix="/v1/manager",
    tags=["manager"],
)


@router.put(
    "/users/{user_id}/verify_status",
    response_model=SuccessResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(is_admin)],
)
async def update_user_verify_status(
    user_id: str,
    data: VerifyStatusSet,
    manager_service: ManagerService = Depends(),
) -> SuccessResponse:
    await manager_service.update_user_verified_status(user_id, data.status)
    return SuccessResponse()


@router.get(
    "/users/",
    response_model=List[models.UserPrivateDTO],
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(is_admin)],
)
async def get_users(
    manager_service: ManagerService = Depends(),
) -> List[models.UserPrivateDTO]:
    users = await manager_service.get_all_users()
    return users


@router.put(
    "/tender/{tender_id}/verify",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
    },
    dependencies=[Depends(is_admin)],
)
async def update_tender_verified_status(
    tender_id: int,
    data: VerifyStatusSet,
    manager_service: ManagerService = Depends(),
) -> SuccessResponse:
    await manager_service.update_tender_verified_status(
        tender_id=tender_id, status=data.status
    )
    return SuccessResponse()
