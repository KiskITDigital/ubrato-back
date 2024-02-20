from models import user_model
from sqlalchemy import Boolean, DateTime, SmallInteger, String, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = mapped_column(String, primary_key=True)
    brand_name = mapped_column(String)
    inn = mapped_column(String)
    email = mapped_column(String)
    phone = mapped_column(String)
    password = mapped_column(String)
    first_name = mapped_column(String)
    middle_name = mapped_column(String)
    last_name = mapped_column(String)
    verify = mapped_column(Boolean, default=False)
    role = mapped_column(SmallInteger, default=0)
    created_at = mapped_column(DateTime, default=func.current_timestamp())

    def to_model(self) -> user_model.User:
        return user_model.User(
            id=self.id,
            brand_name=self.brand_name,
            inn=self.inn,
            email=self.email,
            phone=self.phone,
            password=self.password,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            verify=self.verify,
            role=self.role,
            create_date=self.created_at,
        )
