from typing import List

from models.user import UserMe
from pydantic import BaseModel


class QuestionnaireAnswer(BaseModel):
    id: int
    answers: List[str]
    user: UserMe
