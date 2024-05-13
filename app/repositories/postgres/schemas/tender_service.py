from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
    tender_service_type = relationship(
        "TenderServiceType", back_populates="tender_service_type"
    )
    draft_service_group = relationship(
        "DraftTenderServiceType", back_populates="service_type"
    )
    contractor_services = relationship(
        "ContractorService", back_populates="service_type"
    )


class TenderServiceType(Base):
    __tablename__ = "tender_services_types"

    tender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tender.id"), primary_key=True
    )
    service_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services_types.id"), primary_key=True
    )

    tender_service_type = relationship(
        "ServiceType", back_populates="tender_service_type"
    )
    tender = relationship("Tender", back_populates="tender_service_type")
