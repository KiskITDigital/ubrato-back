import uuid

import bcrypt
import models
from fastapi import Depends
from repositories import UserRepository
from repositories.schemas import Organization, User


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
        avatar: str,
        org: Organization,
    ) -> models.User:
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
            avatar=avatar,
        )

        created_user = self.user_repository.create(user=user, org=org)

        return created_user

    def get_by_email(self, email: str) -> models.User:
        user = self.user_repository.get_by_email(email)

        return user

    def get_by_id(self, id: str) -> models.UserPrivateDTO:
        user = self.user_repository.get_by_id(id)

        return models.UserPrivateDTO(**user.__dict__)

    def password_valid(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def upd_avatar(self, used_id: str, avatar: str) -> None:
        self.user_repository.update_avatar(user_id=used_id, avatar=avatar)
