from pydantic import BaseModel


class Detail(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Detail
