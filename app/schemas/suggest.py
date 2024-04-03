from typing import List, Tuple

from pydantic import BaseModel


class SuggestRespone(BaseModel):
    suggestions: List[Tuple[str, str]]
