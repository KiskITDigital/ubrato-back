from typing import Annotated

from exceptions import ServiceException
from fastapi import APIRouter, Cookie, Depends, Response, status
from routers.v1.exceptions import (
    INVALID_CREDENTIAL,
    USER_ALREADY_EXIST,
    USER_EMAIL_NOT_FOUND,
)
from schemas.exception import ExceptionResponse
from schemas.sign_up import SignUpRequest, SignUpResponse
from schemas.sing_in import SignInRequest, SignInResponse
from services import (
    JWTService,
    LogsService,
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
    logs_service: LogsService = Depends(),
) -> SignUpResponse:
    _, err = user_service.get_by_email(user.email)
    if err is None:
        raise ServiceException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USER_ALREADY_EXIST,
            logs_service=logs_service,
        )

    created_user, err = user_service.create(
        user.email,
        user.phone,
        user.password,
        user.first_name,
        user.middle_name,
        user.last_name,
    )

    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )

    err = org_service.save_organization(inn=user.inn, user_id=created_user.id)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )

    session_id, err = session_service.create_session(created_user.id)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="none",
        secure=True,
    )

    return SignUpResponse(access_token=jwt_service.generate_jwt(created_user))


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
    jwt_service: JWTService = Depends(),
    session_service: SessionService = Depends(),
    logs_service: LogsService = Depends(),
) -> SignInResponse:
    user, err = user_service.get_by_email(data.email)
    if user is None:
        raise ServiceException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_EMAIL_NOT_FOUND.format(data.email),
            logs_service=logs_service,
        )

    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )

    if not user_service.password_valid(data.password, user.password):
        raise ServiceException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIAL,
            logs_service=logs_service,
        )

    session_id, err = session_service.create_session(user.id)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
            logs_service=logs_service,
        )
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="none",
        secure=True,
    )

    return SignInResponse(access_token=jwt_service.generate_jwt(user))


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
    jwt_service: JWTService = Depends(),
    session_service: SessionService = Depends(),
    logs_service: LogsService = Depends(),
) -> SignInResponse:
    user, err = session_service.get_user_session_by_id(session_id=session_id)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err,
            logs_service=logs_service,
        )
    return SignInResponse(access_token=jwt_service.generate_jwt(user))
