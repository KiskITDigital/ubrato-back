from pydantic import BaseModel


class UpdAvatarRequest(BaseModel):
    avatar: str
