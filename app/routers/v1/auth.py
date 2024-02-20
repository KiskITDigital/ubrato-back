from fastapi import APIRouter, Depends, HTTPException, status
from schemas.exception import ErrorResponse
from schemas.sign_up import SignUpRequest, SignUpResponse
from schemas.sing_in import SignInRequest, SignInResponse
from services.jwt import JWTService
from services.user import UserService

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    # dependencies=[Depends(get_bearer_header)],
    # responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}},
)


@router.post(
    "/signup",
    response_model=SignUpResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}
    },
)
async def signup_user(
    user: SignUpRequest, user_service: UserService = Depends()
):
    err = user_service.create(
        user.brand_name,
        user.inn,
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
            detail={"description": err},
        )

    return SignUpResponse(status=True)


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
):
    user, err = user_service.get_by_email(data.email)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"description": err},
        )

    if not user_service.password_valid(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"description": "invalid email or password"},
        )

    return SignInResponse(access_token=jwt_service.generate_jwt(user))
