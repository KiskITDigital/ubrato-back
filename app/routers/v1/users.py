import models
from fastapi import APIRouter, Depends, status
from routers.v1.dependencies import authorized, get_user
from schemas.exception import ExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.success import SuccessResponse
from schemas.upd_avatar import UpdAvatarRequest
from schemas.verify_request import VerifyRequest
from services import OrganizationService, UserService

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
    org_service: OrganizationService = Depends(),
) -> SuccessResponse:
    await org_service.save_docs(links=data.documents, org_id=data.org_id)

    return SuccessResponse()


@router.get(
    "/me",
    response_model=models.UserMe,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_me(
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
) -> models.UserMe:
    dto_user = await user_service.get_by_id(user.id)

    dto_org = models.OrganizationLiteDTO(
        id=user.org_id,
        short_name=user.org_short_name,
        inn=user.org_inn,
        okpo=user.org_okpo,
        ogrn=user.org_ogrn,
        kpp=user.org_kpp,
    )

    return models.UserMe(organiztion=dto_org, **dto_user.__dict__)


@router.put(
    "/me/avatar",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def upd_avatar(
    avatar: UpdAvatarRequest,
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await user_service.upd_avatar(user_id=user.id, avatar=avatar.avatar)
    return SuccessResponse()
