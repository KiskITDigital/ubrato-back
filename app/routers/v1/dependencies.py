from typing import Annotated, Optional

from config import get_config
from exceptions import ServiceException
from fastapi import Depends, Header, status
from schemas.jwt_user import JWTUser
from services.jwt import JWTService
from services.logs import LogsService


async def authorized(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
    _, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err,
        )


async def get_user(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
    logs_service: LogsService = Depends(),
) -> Optional[JWTUser]:
    user, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err,
            logs_service=logs_service,
        )
    return user


# TODO: rename and make for all roles
async def is_admin(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
    logs_service: LogsService = Depends(),
) -> None:
    user, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise ServiceException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err,
            logs_service=logs_service,
        )

    if user.role < get_config().Role.admin:
        raise ServiceException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no access",
        )
