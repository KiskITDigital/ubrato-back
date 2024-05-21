from typing import List, Optional

from repositories.postgres.schemas.base import Base
from sqlalchemy import ARRAY, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CustomerProfile(Base):
    __tablename__ = "customer_profile"

    org_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id"), primary_key=True
    )
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    org = relationship("Organization", back_populates="customer_profile")


class CustomerLocation(Base):
    __tablename__ = "customer_locations"

    org_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id"), primary_key=True
    )
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), primary_key=True
    )

    org = relationship(
        "Organization", back_populates="customer_locations", lazy="selectin"
    )
    city = relationship(
        "City", back_populates="customer_locations", lazy="selectin"
    )


class ContractorProfile(Base):
    __tablename__ = "contractor_profile"

    org_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id"), primary_key=True
    )
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    org = relationship("Organization", back_populates="contractor_profile")


class ContractorService(Base):
    __tablename__ = "contractor_services"

    org_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id"), primary_key=True
    )
    service_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services_types.id"), primary_key=True
    )
    price: Mapped[int] = mapped_column(Integer)

    org = relationship("Organization", back_populates="contractor_services")
    service_type = relationship(
        "ServiceType", back_populates="contractor_services", lazy="selectin"
    )


class ContractorObject(Base):
    __tablename__ = "contractor_objects"

    org_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id"), primary_key=True
    )
    object_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("objects_types.id"), primary_key=True
    )

    org = relationship("Organization", back_populates="contractor_objects")
    object_type = relationship(
        "ObjectType", back_populates="contractor_objects", lazy="selectin"
    )


class ContractorCV(Base):
    __tablename__ = "contractor_cv"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String)
    links: Mapped[List[str]] = mapped_column(ARRAY(String))

    org = relationship("Organization", back_populates="contractor_cv")


class ContractorLocation(Base):
    __tablename__ = "contractor_locations"

    org_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id"), primary_key=True
    )
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), primary_key=True
    )

    org = relationship(
        "Organization", back_populates="contractor_locations", lazy="selectin"
    )
    city = relationship(
        "City", back_populates="contractor_locations", lazy="selectin"
    )
