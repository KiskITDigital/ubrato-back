from typing import Annotated

import models
from exceptions import ServiceException
from fastapi import APIRouter, Cookie, Depends, Response, status
from routers.v1.exceptions import INVALID_CREDENTIAL, NO_COOKIE
from schemas.exception import ExceptionResponse
from schemas.sign_up import SignUpRequest, SignUpResponse
from schemas.sing_in import SignInRequest, SignInResponse
from services import (
    JWTService,
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
            detail=INVALID_CREDENTIAL,
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
            detail=NO_COOKIE,
        )
    user = await session_service.get_user_session_by_id(session_id=session_id)
    org = await org_service.get_organization_by_user_id(user.id)

    return SignInResponse(
        access_token=jwt_service.generate_jwt(
            user=user, org=models.Organization(**org.__dict__)
        )
    )
