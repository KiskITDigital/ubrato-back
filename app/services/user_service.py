from typing import Optional
import uuid
import bcrypt

from fastapi import Depends
from models.user_model import User
from repositories.user_repository import UserRepository


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self.user_repository = user_repository

    def create(self, user: User) -> Optional[Exception]:
        user.password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = user.to_shema()
        user.id = "usr_" + str(uuid.uuid4())

        return self.user_repository.create(user)

    # TODO: JWT!
    def get_by_email(
        self, email: str, password: str
    ) -> tuple[bool, Optional[Exception]]:
        user, err = self.user_repository.get_by_email(email)

        if err is not None:
            return None, err

        if user is None:
            return None, "user not found"

        return (
            bcrypt.checkpw(
                password.encode("utf-8"), user.password.encode("utf-8")
            ),
            None,
        )
