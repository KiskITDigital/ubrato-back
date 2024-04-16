from typing import List

from pydantic import BaseModel

from .user import UserMe


class QuestionnaireAnswer(BaseModel):
    id: int
    answers: List[str]
    user: UserMe
