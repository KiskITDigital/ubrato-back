from typing import Annotated

from config import get_config
from exceptions import AuthException
from fastapi import Depends, Header, status
from schemas.jwt_user import JWTUser
from services import JWTService

localization = get_config().Localization.config


async def authorized(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
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
    user = jwt_service.unmarshal_jwt(authorization)

    if user.role < get_config().Role.admin:
        raise AuthException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=localization["errors"]["no_access"],
        )


async def is_creator_or_manager(
    user_id: str,
    user: JWTUser,
) -> None:
    if user.role < get_config().Role.manager and user.id != user_id:
        raise AuthException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=localization["errors"]["no_access"],
        )
