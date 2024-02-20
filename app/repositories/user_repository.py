from datetime import datetime
from typing import Optional

from fastapi import Depends
from models import user_model
from repositories.database import get_db_connection
from repositories.schemas import User
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    db: scoped_session

    def __init__(
        self,
        db: scoped_session = Depends(get_db_connection)
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
            id=id,
            brand_name=brand_name,
            inn=inn,
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            verify=False,
            role=0<<0,
            created_at=datetime.now() 
        )

        try:
            self.db.add(user)
            self.db.commit()
            return None
        except SQLAlchemyError as err:
            return Exception(err.code)

    def get_by_email(
        self, email: str
    ) -> tuple[Optional[user_model.User], Optional[Exception]]:
        try:
            query = self.db.query(User).filter(User.email == email)
            user = query.first()
            if user is not None:
                return user.to_model(), None
            return None, Exception("user not found")
        except SQLAlchemyError as err:
            return None, Exception(err.code)
