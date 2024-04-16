from typing import List

from fastapi import Depends
from repositories.postgres import QuestionnaireRepository
from schemas import models
from tools import convert_json_to_csv


class QuestionnaireService:
    questionnaire_repository: QuestionnaireRepository

    def __init__(
        self, questionnaire_repository: QuestionnaireRepository = Depends()
    ) -> None:
        self.questionnaire_repository = questionnaire_repository

    async def save(self, answers: List[str], user_id: str) -> None:
        await self.questionnaire_repository.save(
            answers=answers, user_id=user_id
        )

    async def get_page(
        self, page: int, page_size: int
    ) -> List[models.QuestionnaireAnswer]:
        return await self.questionnaire_repository.get_page(
            page=page, page_size=page_size
        )

    async def get_by_user_id(self, user_id: str) -> models.QuestionnaireAnswer:
        return await self.questionnaire_repository.get_by_user_id(
            user_id=user_id
        )

    async def export_csv(self) -> str:
        answers = await self.questionnaire_repository.get_all()
        dict_answers = [answer.model_dump() for answer in answers]
        return convert_json_to_csv(dict_answers)
