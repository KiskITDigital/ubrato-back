from typing import List

from pydantic import BaseModel


class SuggestRespone(BaseModel):
    suggestions: List[str]
