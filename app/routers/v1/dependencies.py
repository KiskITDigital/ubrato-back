from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from config import get_config

from services.jwt import JWTService


async def authorized(authorization: Annotated[str, Header()], jwt_service: JWTService = Depends()) -> None:
    header = authorization.split(" ", 1)
    if header[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Bearer token invalid")
    user, err = jwt_service.decode_jwt(header[1])
    if err is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"description": "access token invalid"})
    

async def super_admin(authorization: Annotated[str, Header()], jwt_service: JWTService = Depends(), ) -> None:
    header = authorization.split(" ", 1)
    if header[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Bearer token invalid")
    user, err = jwt_service.decode_jwt(header[1])
    if err is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"description": "access token invalid"})
    
    if user['role'] < get_config().Role.super_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"description": "no access"})
