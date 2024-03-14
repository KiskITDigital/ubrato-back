from typing import List, Optional, Tuple

import models
from fastapi import Depends
from repositories.database import get_db_connection
from repositories.exceptions import USER_EMAIL_NOT_FOUND, USERID_NOT_FOUND
from repositories.schemas import Document, Organization, User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session


class UserRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(
        self, user: User
    ) -> Tuple[models.User, Optional[Exception]]:
        try:
            self.db.add(user)
            self.db.commit()

            self.db.refresh(user)
            return user.to_model(), None
        except SQLAlchemyError as err:
            return models.User, Exception(err.code)

    def get_by_email(
        self, email: str
    ) -> Tuple[models.User, Optional[Exception]]:
        try:
            query = self.db.query(User).filter(User.email == email)
            user = query.first()
            if user is not None:
                return user.to_model(), None
            return models.User, Exception(USER_EMAIL_NOT_FOUND.format(email))
        except SQLAlchemyError as err:
            return models.User, Exception(err.code)

    def save_verify_info(
        self,
        org: Organization,
        documents: List[Document],
    ) -> Optional[Exception]:
        try:
            self.db.add(org)
            for document in documents:
                self.db.add(document)
            self.db.commit()
            return None
        except SQLAlchemyError as err:
            return Exception(err.code)

    def update_verify_status(
        self, user_id: str, status: bool
    ) -> Optional[Exception]:
        try:
            user = self.db.query(User).filter_by(id=user_id).first()

            if user:
                user.verify = status
                self.db.commit()
                return None

            return Exception(USERID_NOT_FOUND.format(user_id))
        except SQLAlchemyError as err:
            self.db.rollback()
            return Exception(err.code)

    def get_all_users(
        self,
    ) -> Tuple[List[models.User], Optional[Exception]]:
        try:
            query = self.db.query(User)
            users: List[models.User] = []

            for user in query:
                users.append(user.to_model())

            return users, None
        except SQLAlchemyError as err:
            return [], Exception(err.code)

    def get_by_id(
        self, user_id: str
    ) -> Tuple[models.User, Optional[Exception]]:
        try:
            user = self.db.query(User).filter_by(id=user_id).first()

            if user:
                return user.to_model(), None

            return models.User, Exception(USERID_NOT_FOUND.format(user_id))
        except SQLAlchemyError as err:
            self.db.rollback()
            return models.User, Exception(err.code)
