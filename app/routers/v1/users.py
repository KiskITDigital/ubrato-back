import models
from exceptions import ServiceException
from fastapi import APIRouter, Depends, status
from routers.v1.dependencies import authorized, get_user
from schemas.exception import ExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.success import SuccessResponse
from schemas.verify_request import VerifyRequest
from services import LogsService, UserService

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)


@router.post(
    "/me/verify",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def user_requires_verification(
    data: VerifyRequest,
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
    logs_service: LogsService = Depends(),
) -> SuccessResponse:
    err = user_service.user_requires_verification(
        user_id=user.id,
        brand_name=data.brand_name,
        short_name=data.short_name,
        inn=data.inn,
        okpo=data.okpo,
        orgn=data.orgn,
        kpp=data.kpp,
        tax_code=data.tax_code,
        real_address=data.real_address,
        registered_address=data.registered_address,
        mail_address=data.mail_address,
        links=data.documents,
    )

    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )

    return SuccessResponse()


@router.get(
    "/me",
    response_model=models.UserPrivateDTO,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_me(
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
    logs_service: LogsService = Depends(),
) -> models.UserPrivateDTO:
    user, err = user_service.get_by_id(user.id)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )

    return user
