import uuid
from typing import List, Optional

import bcrypt
from fastapi import Depends
from models import user_model
from repositories.user_repository import UserRepository


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
    ) -> Optional[Exception]:
        id = "usr_" + str(uuid.uuid4())

        password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        return self.user_repository.create(
            id,
            email,
            phone,
            password,
            first_name,
            middle_name,
            last_name,
        )

    def get_by_email(
        self, email: str
    ) -> tuple[Optional[user_model.User], Optional[Exception]]:
        user, err = self.user_repository.get_by_email(email)

        if err is not None:
            return None, err

        if user is None:
            return None, Exception("user not found")

        return user, None

    def password_valid(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def user_requires_verification(
        self,
        user_id: str,
        brand_name: str,
        short_name: str,
        inn: int,
        okpo: int,
        orgn: int,
        kpp: int,
        tax_code: int,
        real_address: str,
        registered_address: str,
        mail_address: str,
        documents: List[str],
    ) -> Optional[Exception]:
        id = "org_" + str(uuid.uuid4())
        documents_with_ids = [
            (f"doc_{uuid.uuid4()}", doc) for doc in documents
        ]
        return self.user_repository.save_verify_info(
            user_id,
            id,
            brand_name,
            short_name,
            str(inn),
            str(okpo),
            str(orgn),
            str(kpp),
            tax_code,
            real_address,
            registered_address,
            mail_address,
            documents_with_ids,
        )
