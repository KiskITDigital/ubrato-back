from typing import Annotated

from fastapi import Header, HTTPException


async def get_bearer_header(authorization: Annotated[str, Header()]):
    header = authorization.split(" ", 1)
    if header[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Bearer token invalid")
