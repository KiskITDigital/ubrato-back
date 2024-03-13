from pydantic import BaseModel


class ExceptionResponse(BaseModel):
    id: str
    msg: str


class UnauthExceptionResponse(BaseModel):
    msg: str
