from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DraftTenderServiceType(Base):
    __tablename__ = "draft_tender_services_types"

    tender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("draft_tender.id"), primary_key=True
    )
    service_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services_types.id"), primary_key=True
    )

    service_type = relationship(
        "ServiceType", back_populates="draft_service_group"
    )
    draft_tender = relationship(
        "DraftTender", back_populates="draft_tender_service_type"
    )
