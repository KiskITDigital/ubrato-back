from typing import List, Optional, Tuple

from fastapi import Depends
from models import user_model
from repositories.database import get_db_connection
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
    ) -> Tuple[Optional[user_model.User], Optional[Exception]]:
        try:
            self.db.add(user)
            self.db.commit()

            self.db.refresh(user)
            return user.to_model(), None
        except SQLAlchemyError as err:
            return None, Exception(err.code)

    def get_by_email(
        self, email: str
    ) -> Tuple[Optional[user_model.User], Optional[Exception]]:
        try:
            query = self.db.query(User).filter(User.email == email)
            user = query.first()
            if user is not None:
                return user.to_model(), None
            return None, Exception("user not found")
        except SQLAlchemyError as err:
            return None, Exception(err.code)

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

            return Exception("User with ID {} not found.".format(user_id))
        except SQLAlchemyError as err:
            self.db.rollback()
            return Exception(err.code)

    def get_all_users(
        self
    ) -> Tuple[List[user_model.User], Optional[Exception]]:
        try:
            query = self.db.query(User)
            users: List[user_model.User] = []

            for user in query:
                users.append(user.to_model())

            return users, None
        except SQLAlchemyError as err:
            return [], Exception(err.code)
        
    def get_by_id(
        self, user_id: str
    ) -> Tuple[Optional[user_model.User], Optional[Exception]]:
        try:
            user = self.db.query(User).filter_by(id=user_id).first()

            if user:
                return user.to_model(), None

            return None, Exception("User with ID {} not found.".format(user_id))
        except SQLAlchemyError as err:
            self.db.rollback()
            return None, Exception(err.code)