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
        self,
        id: str,
        email: str,
        phone: str,
        password: str,
        first_name: str,
        middle_name: str,
        last_name: str,
    ) -> Optional[Exception]:
        user = User(
            id=id,
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
        )

        try:
            self.db.add(user)
            self.db.commit()

            # TODO: return user and generate session
            # self.db.refresh(author)
            # return author

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

    def save_verify_info(
        self,
        user_id: str,
        id: str,
        brand_name: str,
        short_name: str,
        inn: str,
        okpo: str,
        orgn: str,
        kpp: str,
        tax_code: int,
        real_address: str,
        registered_address: str,
        mail_address: str,
        documents: List[Tuple[str, str]],
    ) -> Optional[Exception]:
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

        try:
            self.db.add(org)
            for doc_id, link in documents:
                document = Document(
                    id=doc_id,
                    url=link,
                    organization_id=id,
                )
                self.db.add(document)

            self.db.commit()
            return None
        except SQLAlchemyError as err:
            return Exception(err.code)
