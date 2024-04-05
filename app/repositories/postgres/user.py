from typing import List

import models
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import (
    USER_EMAIL_NOT_FOUND,
    USERID_NOT_FOUND,
    RepositoryException,
)
from repositories.postgres.schemas import Organization, User
from sqlalchemy.orm import Session, scoped_session


class UserRepository:
    db: scoped_session[Session]

    def __init__(
        self, db: scoped_session[Session] = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, user: User, org: Organization) -> models.User:
        self.db.add(user)
        self.db.flush()
        org.user_id = user.id
        self.db.add(org)
        self.db.commit()

        self.db.refresh(user)

        return models.User(**user.__dict__)

    def get_by_email(self, email: str) -> models.User:
        query = self.db.query(User).filter(User.email == email)
        user = query.first()
        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_EMAIL_NOT_FOUND.format(email),
                sql_msg="",
            )

        return models.User(**user.__dict__)

    def update_verified_status(self, user_id: str, verified: bool) -> None:
        user = self.db.query(User).filter_by(id=user_id).first()

        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USERID_NOT_FOUND.format(user_id),
                sql_msg="",
            )

        user.verified = verified
        self.db.commit()

    def get_all_users(
        self,
    ) -> List[models.User]:
        query = self.db.query(User)
        users: List[models.User] = []

        for user in query:
            users.append(models.User(**user.__dict__))

        return users

    def get_by_id(self, user_id: str) -> models.User:
        user = self.db.query(User).filter_by(id=user_id).first()

        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USERID_NOT_FOUND.format(user_id),
                sql_msg="",
            )

        return models.User(**user.__dict__)

    def update_avatar(self, user_id: str, avatar: str) -> None:
        user = self.db.query(User).filter_by(id=user_id).first()

        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USERID_NOT_FOUND.format(user_id),
                sql_msg="",
            )

        user.avatar = avatar
        self.db.commit()
