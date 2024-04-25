from typing import Optional

from pydantic import BaseModel


class VerifyStatusSet(BaseModel):
    status: bool
    message: Optional[str]
