from exceptions import (
    INVALID_CREDENTIAL,
    USER_ALREADY_EXIST,
    USER_EMAIL_NOT_FOUND,
    ServiceException,
)
from fastapi import APIRouter, Depends, status
from schemas.exception import ExceptionResponse
from schemas.sign_up import SignUpRequest, SignUpResponse
from schemas.sing_in import SignInRequest, SignInResponse
from services.jwt import JWTService
from services.logs import LogsService
from services.user import UserService

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
)


@router.post(
    "/signup",
    response_model=SignUpResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionResponse},
    },
)
async def signup_user(
    user: SignUpRequest,
    user_service: UserService = Depends(),
    jwt_service: JWTService = Depends(),
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

    return SignUpResponse(access_token=jwt_service.generate_jwt(created_user))


@router.post(
    "/signin",
    response_model=SignInResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionResponse},
    },
)
async def signin_user(
    data: SignInRequest,
    user_service: UserService = Depends(),
    jwt_service: JWTService = Depends(),
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

    return SignInResponse(access_token=jwt_service.generate_jwt(user))
