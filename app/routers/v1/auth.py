from fastapi import APIRouter, Depends, HTTPException, status
from routers.v1.dependencies import authorized, get_user
from schemas.exception import ErrorResponse
from schemas.jwt_user import JWTUser
from schemas.sign_up import SignUpRequest, SignUpResponse
from schemas.sing_in import SignInRequest, SignInResponse
from schemas.success import SuccessResponse
from schemas.verify_request import VerifyRequest
from services.jwt import JWTService
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
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def signup_user(
    user: SignUpRequest,
    user_service: UserService = Depends(),
    jwt_service: JWTService = Depends(),
) -> SignUpResponse:
    _, err = user_service.get_by_email(user.email)
    if err is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"description": "user already exist"},
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"description": str(err)},
        )

    return SignUpResponse(access_token=jwt_service.generate_jwt(created_user))


@router.post(
    "/signin",
    response_model=SignInResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
    },
)
async def signin_user(
    data: SignInRequest,
    user_service: UserService = Depends(),
    jwt_service: JWTService = Depends(),
) -> SignInResponse:
    user, err = user_service.get_by_email(data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"description": "user not found"},
        )

    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"description": str(err)},
        )

    if not user_service.password_valid(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"description": "invalid email or password"},
        )

    return SignInResponse(access_token=jwt_service.generate_jwt(user))


@router.post(
    "/verify",
    response_model=SuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
    dependencies=[Depends(authorized)],
)
async def user_requires_verification(
    data: VerifyRequest,
    user_service: UserService = Depends(),
    user: JWTUser = Depends(get_user),
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"description": str(err)},
        )

    return SuccessResponse()
