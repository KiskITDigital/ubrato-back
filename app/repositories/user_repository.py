from typing import Optional

from fastapi import Depends
from models import user_model
from repositories.database import get_db_connection
from repositories.schemas import User
from sqlalchemy.orm import scoped_session


class UserRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(
        self,
        id: str,
        brand_name: str,
        inn: str,
        email: str,
        phone: str,
        password: str,
        first_name: str,
        middle_name: str,
        last_name: str,
    ) -> Optional[Exception]:
        user = User(
            id,
            brand_name,
            inn,
            email,
            phone,
            password,
            first_name,
            middle_name,
            last_name,
            None,
            None,
            None,
        )

        try:
            self.db.add(user)
            self.db.commit()
            return None
        except Exception as err:
            return err

    def get_by_email(
        self, email: str
    ) -> tuple[Optional[user_model.User], Optional[Exception]]:
        try:
            query = self.db.query(User).filter(User.email == email)
            return query.first().to_model(), None
        except Exception as err:
            return None, err
