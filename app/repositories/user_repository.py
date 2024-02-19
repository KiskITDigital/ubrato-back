from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import scoped_session
from configs.database import get_db_connection
from repositories.user_schema import User


class UserRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, user: User) -> Optional[Exception]:
        try:
            self.db.add(user)
            self.db.commit()
            return None
        except Exception as err:
            return err

    def get_by_email(
        self, email: str
    ) -> tuple[Optional[User], Optional[Exception]]:
        try:
            query = self.db.query(User).filter(User.email == email)
            return query.first(), None
        except Exception as err:
            return None, err
