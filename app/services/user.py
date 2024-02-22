import uuid
from typing import List, Optional

import bcrypt
from fastapi import Depends
from models import user_model
from repositories.schemas import Document, Organization, User
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
    ) -> tuple[Optional[user_model.User], Optional[Exception]]:
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

        created_user, err = self.user_repository.create(user)

        if err is not None:
            return None, err

        if created_user is None:
            return None, Exception("internal error when creating a user")

        return created_user, None

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
        links: List[str],
    ) -> Optional[Exception]:
        id = "org_" + str(uuid.uuid4())

        org = Organization(
            id=id,
            brand_name=brand_name,
            short_name=short_name,
            inn=inn,
            okpo=okpo,
            orgn=orgn,
            kpp=kpp,
            tax_code=tax_code,
            real_address=real_address,
            mail_address=mail_address,
            registered_address=registered_address,
            user_id=user_id,
        )

        documents: List[Document] = []

        for link in links:
            document = Document(
                id=f"doc_{uuid.uuid4()}",
                url=link,
                organization_id=id,
            )
            documents.append(document)

        return self.user_repository.save_verify_info(org, documents)
