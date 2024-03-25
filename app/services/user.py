import uuid
from typing import Optional

import bcrypt
import models
from fastapi import Depends
from repositories import UserRepository
from repositories.schemas import Organization, User
from services.exceptions import (
    ERROR_WHILE_CREATE_USER,
    USER_EMAIL_NOT_FOUND,
    USER_NOT_FOUND,
)


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self.user_repository = user_repository

    def create(
        self,
        email: str,
        phone: str,
        password: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        org: Organization,
    ) -> tuple[Optional[models.User], Optional[Exception]]:
        id = "usr_" + str(uuid.uuid4())

        password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            id=id,
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )

        created_user, err = self.user_repository.create(user=user, org=org)

        if err is not None:
            return None, err

        if created_user is None:
            return None, Exception(ERROR_WHILE_CREATE_USER)

        return created_user, None

    def get_by_email(
        self, email: str
    ) -> tuple[Optional[models.User], Optional[Exception]]:
        user, err = self.user_repository.get_by_email(email)

        if err is not None:
            return None, err

        if user is None:
            return None, Exception(USER_EMAIL_NOT_FOUND.format(email))

        return user, None

    def get_by_id(
        self, id: str
    ) -> tuple[models.UserPrivateDTO, Optional[Exception]]:
        user, err = self.user_repository.get_by_id(id)

        if err is not None:
            return None, err

        if user is None:
            return None, Exception(USER_NOT_FOUND)

        return models.UserPrivateDTO(**user.__dict__), None

    def password_valid(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )
