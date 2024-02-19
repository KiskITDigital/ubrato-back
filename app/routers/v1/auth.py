from fastapi import APIRouter, Depends, HTTPException, status
from schemas.sign_up import SignUpSchema
from schemas.sing_in import SignInSchema

from services.user_service import UserService

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    # dependencies=[Depends(get_bearer_header)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/signup")
async def signup_user(
    user: SignUpSchema, user_service: UserService = Depends()
):
    err = user_service.create(user)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"err": err},
        )
    # TODO: impl jwt gen
    return {"status": "ok"}


@router.post("/signin")
async def signin_user(
    user: SignInSchema, user_service: UserService = Depends()
):
    sts, err = user_service.get_by_email(user.email, user.password)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"description": err},
        )
    return {"status": sts}
