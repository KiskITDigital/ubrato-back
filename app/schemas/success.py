from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status: bool = True
