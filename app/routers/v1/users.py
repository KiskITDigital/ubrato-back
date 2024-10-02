from typing import List

from fastapi import APIRouter, Depends, status
from repositories.postgres.exceptions import RepositoryException
from routers.v1.dependencies import authorized, get_user
from schemas import models
from schemas.exception import ExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.offer_tender import OfferTenderRequest
from schemas.success import SuccessResponse
from schemas.update_profile import UpdateUserInfoRequest, UpdAvatarRequest
from services import (
    NoticeService,
    OrganizationService,
    QuestionnaireService,
    TenderService,
    UserService,
    VerificationService,
)

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)


@router.get(
    "/me/verify",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
    tags=["users", "verification"],
)
async def user_requires_verification(
    verf_service: VerificationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await verf_service.create_verification_requests(user_id=user.id)
    return SuccessResponse()


@router.get(
    "/me/verification/history",
    response_model=List[models.VerificationInfo],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
    tags=["users", "verification"],
)
async def user_verification_history(
    verf_service: VerificationService = Depends(),
    user: JWTUser = Depends(get_user),
) -> List[models.VerificationInfo]:
    return await verf_service.get_verification_history(user_id=user.id)


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


@router.get(
    "/me/pass-questionnaire",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def pass_questionnaire(
    questionnaire_service: QuestionnaireService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    try:
        await questionnaire_service.get_by_user_id(user_id=user.id)
        return SuccessResponse()
    except RepositoryException as err:
        if err.status_code == status.HTTP_404_NOT_FOUND:
            return SuccessResponse(status=False)
        raise err


@router.get(
    "/me/notice",
    response_model=models.Notifications,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def get_notice(
    notice_service: NoticeService = Depends(),
    user: JWTUser = Depends(get_user),
) -> models.Notifications:
    return await notice_service.get_user_notice(user_id=user.id)


@router.put(
    "/me/notice/read",
    response_model=SuccessResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
    description="many values example usage: /me/notice/read?ids_str=1,2,3",
)
async def mark_read_notice(
    ids_str: str,
    notice_service: NoticeService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    ids = [int(x) for x in ids_str.split(",")]

    await notice_service.mark_read(ids=ids, user_id=user.id)
    return SuccessResponse()


@router.post(
    "/{contractor_id}/add_favorite",
    response_model=SuccessResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def add_favorite_contractor(
    contractor_id: str,
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await user_service.add_favorite_contratctor(
        user_id=user.id, contractor_id=contractor_id
    )
    return SuccessResponse()


@router.post(
    "/{contractor_id}/remove_favorite",
    response_model=SuccessResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def remove_favorite_contractor(
    contractor_id: str,
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await user_service.remove_favorite_contratctor(
        user_id=user.id, contractor_id=contractor_id
    )
    return SuccessResponse()


@router.get(
    "/{contractor_id}/is_favorite",
    response_model=SuccessResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def is_favorite_contractor(
    contractor_id: str,
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    return SuccessResponse(
        status=await user_service.is_favorite_contratctor(
            user_id=user.id, contractor_id=contractor_id
        )
    )


@router.get(
    "/me/favorite_contractors",
    response_model=List[models.FavoriteContractor],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def list_favorite_contractor(
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
) -> List[models.FavoriteContractor]:
    return await user_service.list_favorite_contratctor(user_id=user.id)


@router.post(
    "/{contractor_id}/offer",
    response_model=SuccessResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def offer_tender(
    contractor_id: str,
    data: OfferTenderRequest,
    tender_service: TenderService = Depends(),
    org_service: OrganizationService = Depends(),
    notice_service: NoticeService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await tender_service.make_offer(
        contractor_id=contractor_id, tender_id=data.tender_id, user_id=user.id
    )
    org = await org_service.get_organization_by_id(org_id=contractor_id)
    await notice_service.add_notice(
        user_id=org.user_id,
        header="Оффер",
        msg="Вы получиле оффер",
        href=f"https://ubrato.ru/tender/{data.tender_id}",
        href_text="посмотреть тендер",
        href_color=1,
    )
    return SuccessResponse()


@router.get(
    "/me/favorite_tenders",
    response_model=List[models.Tender],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def list_favorite_tenders(
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
) -> List[models.Tender]:
    return await user_service.list_favorite_tenders(user_id=user.id)


@router.put(
    "/me/info",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def update_user_info(
    data: UpdateUserInfoRequest,
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    await user_service.upd_info(
        user_id=user.id,
        first_name=data.first_name,
        middle_name=data.middle_name,
        last_name=data.last_name,
        phone=data.phone,
    )
    return SuccessResponse()
