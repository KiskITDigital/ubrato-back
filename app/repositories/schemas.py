from models import user_model
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = mapped_column(String(41), primary_key=True)
    email = mapped_column(String(255), nullable=False)
    phone = mapped_column(String(20), nullable=False)
    password = mapped_column(String(255), nullable=False)
    first_name = mapped_column(String(100), nullable=False)
    middle_name = mapped_column(String(100), nullable=False)
    last_name = mapped_column(String(100), nullable=False)
    verify = mapped_column(Boolean, default=False)
    role = mapped_column(SmallInteger, default=0)
    created_at = mapped_column(DateTime, default=func.current_timestamp())

    organization = relationship("Organization", back_populates="user")

    def to_model(self) -> user_model.User:
        return user_model.User(
            id=self.id,
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


class Organization(Base):
    __tablename__ = "organizations"

    id = mapped_column(String(40), primary_key=True)
    brand_name = mapped_column(String(255), nullable=False)
    short_name = mapped_column(String(50), nullable=False)
    inn = mapped_column(String(12), nullable=False)
    okpo = mapped_column(String(12), nullable=False)
    orgn = mapped_column(String(12), nullable=False)
    kpp = mapped_column(String(12), nullable=False)
    tax_code = mapped_column(Integer, nullable=False)
    real_address = mapped_column(String(255), nullable=False)
    registered_address = mapped_column(String(255), nullable=False)
    mail_address = mapped_column(String(255), nullable=False)
    user_id = mapped_column(String(40), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="organization")
    documents = relationship("Document", back_populates="organization")


class Document(Base):
    __tablename__ = "documents"

    id = mapped_column(String(40), primary_key=True)
    url = mapped_column(String(255), nullable=False)
    organization_id = mapped_column(String(40), ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="documents")
