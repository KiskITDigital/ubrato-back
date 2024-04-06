from datetime import datetime
from typing import List

from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    Identity,
    Integer,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# TODO: add info row for admin
class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(41), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[int] = mapped_column(SmallInteger, default=0)
    is_contractor: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.current_timestamp()
    )

    organization = relationship("Organization", back_populates="user")
    tender = relationship("Tender", back_populates="user")
    session = relationship("Session", back_populates="user")


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=False)
    inn: Mapped[str] = mapped_column(String(10), nullable=False)
    okpo: Mapped[str] = mapped_column(String(8), nullable=False)
    ogrn: Mapped[str] = mapped_column(String(15), nullable=False)
    kpp: Mapped[str] = mapped_column(String(12), nullable=False)
    tax_code: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), nullable=False
    )
    update_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )

    user = relationship("User", back_populates="organization")
    documents = relationship("Document", back_populates="organization")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id")
    )

    organization = relationship("Organization", back_populates="documents")


class Tender(Base):
    __tablename__ = "tender"

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, cycle=True), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    is_contract_price: Mapped[bool] = mapped_column(Boolean, nullable=False)
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), nullable=False
    )
    floor_space: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(400))
    wishes: Mapped[str] = mapped_column(String(400))
    attachments: Mapped[List[str]] = mapped_column(ARRAY(Text))
    services_groups: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    services_types: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    reception_start: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )
    reception_end: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )
    work_start: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )
    work_end: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )
    object_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("objects_groups.id")
    )
    object_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("objects_types.id")
    )
    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )
    verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    active: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    user = relationship("User", back_populates="tender")
    object_group = relationship("ObjectGroup", back_populates="tender")
    object_type = relationship("ObjectType", back_populates="tender")
    city = relationship("City")


class ObjectGroup(Base):
    __tablename__ = "objects_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))

    object_type = relationship("ObjectType", back_populates="object_group")
    tender = relationship("Tender", back_populates="object_group")


class ObjectType(Base):
    __tablename__ = "objects_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    object_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("objects_groups.id")
    )

    object_group = relationship("ObjectGroup", back_populates="object_type")
    tender = relationship("Tender", back_populates="object_type")


class ServiceGroup(Base):
    __tablename__ = "services_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))

    service_type = relationship("ServiceType", back_populates="service_group")


class ServiceType(Base):
    __tablename__ = "services_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(90))
    service_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services_groups.id")
    )

    service_group = relationship("ServiceGroup", back_populates="service_type")


class Logs(Base):
    __tablename__ = "logs"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    method: Mapped[str] = mapped_column(String(6), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    msg: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.current_timestamp()
    )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.current_timestamp()
    )

    user = relationship("User", back_populates="session")


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    cities = relationship("City", back_populates="region")


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"))

    region = relationship("Region", back_populates="cities")
    tenders = relationship("Tender", back_populates="city")
