from typing import List

from pydantic import BaseModel


class QuestionnaireRequest(BaseModel):
    answers: List[str]
