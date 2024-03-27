from typing import Annotated

from config import get_config
from exceptions import AuthException
from fastapi import Depends, Header, status
from routers.v1.exceptions import NO_ACCESS
from schemas.jwt_user import JWTUser
from services import JWTService


async def authorized(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
):
    jwt_service.unmarshal_jwt(authorization)


async def get_user(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> JWTUser:
    user = jwt_service.unmarshal_jwt(authorization)
    return user


# TODO: rename and make for all roles
async def is_admin(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
    user, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err,
        )

    if user.role < get_config().Role.admin:
        raise AuthException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NO_ACCESS,
        )


async def is_creator_or_manager(
    user_id: str,
    user: JWTUser,
) -> None:
    if user.role < get_config().Role.manager and user.id != user_id:
        raise AuthException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NO_ACCESS,
        )
