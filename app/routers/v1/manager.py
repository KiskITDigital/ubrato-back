from fastapi import APIRouter, Depends, HTTPException, status
from routers.v1.dependencies import has_permission
from schemas.success import SuccessResponse
from schemas.verify_status_set import VerifyStatusSet
from services.manager import ManagerService

router = APIRouter(
    prefix="/v1/manager",
    tags=["manager"],
)


@router.put(
    "/user/{user_id}/verify_status",
    response_model=SuccessResponse,
    dependencies=[Depends(has_permission)],
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
