from typing import Annotated

from exceptions import ServiceException
from fastapi import APIRouter, Cookie, Depends, Response, status
from routers.v1.dependencies import authorized, get_user, localization
from schemas.change_password import ChangePasswordRequest
from schemas.exception import ExceptionResponse
from schemas.jwt_user import JWTUser
from schemas.sign_up import SignUpRequest, SignUpResponse
from schemas.sing_in import SignInRequest, SignInResponse
from schemas.success import SuccessResponse
from services import (
    JWTService,
    NoticeService,
    OrganizationService,
    SessionService,
    UserService,
)

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
)


@router.post(
    "/signup",
    response_model=SignUpResponse,
    response_description="It also returns a session_id cookie",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def signup_user(
    response: Response,
    user: SignUpRequest,
    user_service: UserService = Depends(),
    org_service: OrganizationService = Depends(),
    jwt_service: JWTService = Depends(),
    session_service: SessionService = Depends(),
    notice_service: NoticeService = Depends(),
) -> SignUpResponse:
    org = org_service.get_organization_from_api(inn=user.inn)

    created_user, created_org = await user_service.create(
        email=user.email,
        phone=user.phone,
        password=user.password,
        first_name=user.first_name,
        middle_name=user.middle_name,
        last_name=user.last_name,
        is_contractor=user.is_contractor,
        avatar=user.avatar,
        org=org,
    )

    session_id = await session_service.create_session(created_user.id)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="none",
        secure=True,
    )

    await notice_service.add_notice(
        user_id=created_user.id,
        header=localization["notice"]["end_of_registration"]["header"],
        msg=localization["notice"]["end_of_registration"]["text"],
        href=None,
        href_text=None,
        href_color=None,
    )

    access_token = jwt_service.generate_auth_jwt(user_id=created_user.id)

    await user_service.ask_confirm_email(
        user_email=created_user.email, salt=access_token
    )

    return SignUpResponse(
        access_token=jwt_service.generate_jwt(created_user, created_org)
    )


@router.post(
    "/signin",
    response_description="It also returns a session_id cookie",
    response_model=SignInResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionResponse},
    },
)
async def signin_user(
    response: Response,
    data: SignInRequest,
    user_service: UserService = Depends(),
    org_service: OrganizationService = Depends(),
    jwt_service: JWTService = Depends(),
    session_service: SessionService = Depends(),
) -> SignInResponse:
    user = await user_service.get_by_email(data.email)

    org = await org_service.get_organization_by_user_id(user.id)

    if not user_service.password_valid(data.password, user.password):
        raise ServiceException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=localization["errors"]["invalid_credential"],
        )

    session_id = await session_service.create_session(user.id)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="none",
        secure=True,
    )

    return SignInResponse(
        access_token=jwt_service.generate_jwt(user=user, org=org)
    )


@router.get(
    "/refresh",
    response_description="Uses the session_id cookie to update the access token",
    response_model=SignInResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionResponse},
    },
)
async def refresh_session(
    session_id: Annotated[str | None, Cookie()],
    org_service: OrganizationService = Depends(),
    jwt_service: JWTService = Depends(),
    session_service: SessionService = Depends(),
) -> SignInResponse:
    if session_id is None:
        raise ServiceException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=localization["errors"]["no_cookie"],
        )
    user = await session_service.get_user_session_by_id(session_id=session_id)
    org = await org_service.get_organization_by_user_id(user.id)

    return SignInResponse(
        access_token=jwt_service.generate_jwt(user=user, org=org)
    )


@router.get(
    "/reset-password",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionResponse},
    },
)
async def ask_reset_password(
    email: str,
    user_service: UserService = Depends(),
) -> SuccessResponse:
    await user_service.ask_reset_pass(email=email)
    return SuccessResponse()


@router.post(
    "/reset-password",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionResponse},
    },
)
async def reset_password(
    data: ChangePasswordRequest,
    user_service: UserService = Depends(),
) -> SuccessResponse:
    await user_service.reset_password(
        email=data.email, password=data.password, code=data.code
    )
    return SuccessResponse()


@router.get(
    "/confirm-email",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionResponse},
    },
    dependencies=[Depends(authorized)],
)
async def ask_email_confirmation(
    user_service: UserService = Depends(),
    jwt_service: JWTService = Depends(),
    user: JWTUser = Depends(get_user),
) -> SuccessResponse:
    access_token = jwt_service.generate_auth_jwt(user_id=user.id)
    user_email = (await user_service.get_by_id(id=user.id)).email

    await user_service.ask_confirm_email(
        user_email=user_email, salt=access_token
    )
    return SuccessResponse()


@router.post(
    "/confirm-email",
    response_model=SuccessResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionResponse},
    },
)
async def confirm_email(
    token: str,
    user_service: UserService = Depends(),
    jwt_service: JWTService = Depends(),
) -> SuccessResponse:
    access_token = jwt_service.decode_auth_jwt(token=token)

    await user_service.confirm_email(user_id=access_token.id)
    return SuccessResponse()
