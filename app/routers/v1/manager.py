from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from models.user_model import User
from routers.v1.dependencies import is_admin
from schemas.success import SuccessResponse
from schemas.verify_status_set import VerifyStatusSet
from services.manager import ManagerService

router = APIRouter(
    prefix="/v1/manager",
    tags=["manager"],
)


@router.put(
    "/users/{user_id}/verify_status",
    response_model=SuccessResponse,
    dependencies=[Depends(is_admin)],
)
async def update_user_verify_status(
    user_id: str,
    data: VerifyStatusSet,
    user_service: ManagerService = Depends(),
) -> SuccessResponse:
    err = user_service.update_verify_status(user_id, data.status)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"description": str(err)},
        )
    return SuccessResponse()


@router.get(
    "/users/",
    response_model=List[User],
    dependencies=[Depends(is_admin)],
)
async def get_users(
    user_service: ManagerService = Depends(),
) -> SuccessResponse:
    users, err = user_service.get_all_users()
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"description": str(err)},
        )
    return users


@router.get(
    "/users/{user_id}",
    response_model=User,
    dependencies=[Depends(is_admin)],
)
async def get_user(
    user_id: str,
    user_service: ManagerService = Depends(),
) -> SuccessResponse:
    user, err = user_service.get_by_id(user_id=user_id)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"description": str(err)},
        )
    return user
