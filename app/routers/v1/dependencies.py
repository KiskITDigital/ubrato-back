from typing import Annotated, Optional

from config import get_config
from fastapi import Depends, Header, HTTPException, status
from schemas.jwt_user import JWTUser
from services.jwt import JWTService


async def authorized(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
    _, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"description": err},
        )


async def get_user(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> Optional[JWTUser]:
    user, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"description": err},
        )
    return user


async def has_permission(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
    user, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"description": err},
        )

    if user.role < get_config().Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"description": "no access"},
        )
