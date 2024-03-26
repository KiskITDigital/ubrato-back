from typing import List

import models
from fastapi import Depends
from repositories.database import get_db_connection
from repositories.exceptions import (
    USER_ALREADY_REG,
    USER_EMAIL_NOT_FOUND,
    USERID_NOT_FOUND,
    RepositoryException,
)
from repositories.schemas import Organization, User
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import scoped_session


class UserRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, user: User, org: Organization) -> models.User:
        try:
            self.db.add(user)
            org.user_id = user.id
            self.db.add(org)
            self.db.commit()

            self.db.refresh(user)

            return models.User(**user.__dict__)
        except IntegrityError:
            self.db.rollback()
            raise RepositoryException(
                status_code=400,
                detail=USER_ALREADY_REG,
                sql_msg="",
            )
        except SQLAlchemyError as err:
            self.db.rollback()
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def get_by_email(self, email: str) -> models.User:
        try:
            query = self.db.query(User).filter(User.email == email)
            user = query.first()
            if user is None:
                raise RepositoryException(
                    status_code=404,
                    detail=USER_EMAIL_NOT_FOUND.format(email),
                    sql_msg="",
                )

            return models.User(**user.__dict__)
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def update_verified_status(self, user_id: str, status: bool):
        try:
            user = self.db.query(User).filter_by(id=user_id).first()

            if user is None:
                raise RepositoryException(
                    status_code=404,
                    detail=USERID_NOT_FOUND.format(user_id),
                    sql_msg="",
                )

            user.verified = status
            self.db.commit()
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def get_all_users(
        self,
    ) -> List[models.User]:
        try:
            query = self.db.query(User)
            users: List[models.User] = []

            for user in query:
                users.append(models.User(**user.__dict__))

            return users
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def get_by_id(self, user_id: str) -> models.User:
        try:
            user = self.db.query(User).filter_by(id=user_id).first()

            if user is None:
                raise RepositoryException(
                    status_code=404,
                    detail=USERID_NOT_FOUND.format(user_id),
                    sql_msg="",
                )

            return models.User(**user.__dict__)
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )
