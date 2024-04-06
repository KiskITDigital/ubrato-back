import uuid
from typing import Tuple

import bcrypt
import models
from fastapi import Depends
from repositories.postgres import UserRepository
from repositories.postgres.schemas import Organization, User


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self.user_repository = user_repository

    async def create(
        self,
        email: str,
        phone: str,
        password: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        is_contractor: bool,
        avatar: str,
        org: Organization,
    ) -> Tuple[models.User, models.Organization]:
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
            is_contractor=is_contractor,
            avatar=avatar,
        )

        created_user, created_org = await self.user_repository.create(
            user=user, org=org
        )

        return created_user, created_org

    async def get_by_email(self, email: str) -> models.User:
        user = await self.user_repository.get_by_email(email)

        return user

    async def get_by_id(self, id: str) -> models.UserPrivateDTO:
        user = await self.user_repository.get_by_id(id)

        return models.UserPrivateDTO(**user.__dict__)

    def password_valid(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    async def upd_avatar(self, user_id: str, avatar: str) -> None:
        await self.user_repository.update_avatar(
            user_id=user_id, avatar=avatar
        )
