from typing import List

from config import get_config
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import RepositoryException
from repositories.postgres.schemas import Organization, Questionnaire, User
from schemas import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class QuestionnaireRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db
        self.localization = get_config().Localization.config

    async def save(self, answers: List[str], user_id: str) -> None:
        self.db.add(
            Questionnaire(
                answers=answers,
                user_id=user_id,
            )
        )
        await self.db.commit()

    async def get_page(
        self, page: int, page_size: int
    ) -> List[models.QuestionnaireAnswer]:
        query = await self.db.execute(
            select(Questionnaire, User, Organization)
            .join(User, Questionnaire.user_id == User.id)
            .join(Organization, Questionnaire.user_id == Organization.user_id)
            .order_by(Questionnaire.created_at.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )

        answers: List[models.QuestionnaireAnswer] = []

        for found_tender in query.all():
            answer, user, org = found_tender._tuple()

            org_model = models.OrganizationLiteDTO(**org.__dict__)
            user_model = models.UserMe(organiztion=org_model, **user.__dict__)

            answers.append(
                models.QuestionnaireAnswer(
                    id=answer.id,
                    answers=answer.answers,
                    user=user_model,
                )
            )

        return answers

    async def get_all(self) -> List[models.QuestionnaireAnswer]:
        query = await self.db.execute(
            select(Questionnaire, User, Organization)
            .join(User, Questionnaire.user_id == User.id)
            .join(Organization, Questionnaire.user_id == Organization.user_id)
            .order_by(Questionnaire.created_at.desc())
        )

        answers: List[models.QuestionnaireAnswer] = []

        for found_tender in query.all():
            answer, user, org = found_tender._tuple()

            org_model = models.OrganizationLiteDTO(**org.__dict__)
            user_model = models.UserMe(organiztion=org_model, **user.__dict__)

            answers.append(
                models.QuestionnaireAnswer(
                    id=answer.id,
                    answers=answer.answers,
                    user=user_model,
                )
            )

        return answers

    async def get_by_user_id(self, user_id: str) -> models.QuestionnaireAnswer:
        query = await self.db.execute(
            select(Questionnaire, User, Organization)
            .join(User, Questionnaire.user_id == User.id)
            .join(Organization, Questionnaire.user_id == Organization.user_id)
            .order_by(Questionnaire.created_at.desc())
            .where(Questionnaire.user_id == user_id)
        )

        result = query.tuples().first()

        if result is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.localization["errors"]["questionnaire_not_found"],
                sql_msg="",
            )

        answer, user, org = result

        org_model = models.OrganizationLiteDTO(**org.__dict__)
        user_model = models.UserMe(organiztion=org_model, **user.__dict__)

        return models.QuestionnaireAnswer(
            id=answer.id,
            answers=answer.answers,
            user=user_model,
        )
