from models import user_model
from sqlalchemy import Boolean, Column, DateTime, SmallInteger, String, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    brand_name = Column(String)
    inn = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    verify = Column(Boolean, default=False)
    role = Column(SmallInteger, default=0)
    created_at = Column(DateTime, default=func.current_timestamp())

    def __init__(
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
        verify: bool,
        role: int,
        created_at: str,
    ):
        self.id = (id,)
        self.brand_name = brand_name
        self.inn = inn
        self.email = email
        self.phone = phone
        self.password = password
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.verify = verify
        self.role = role
        self.created_at = created_at

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
