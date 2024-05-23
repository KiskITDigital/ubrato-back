from datetime import datetime
from typing import Optional

from repositories.postgres.schemas.base import Base
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TenderRespond(Base):
    __tablename__ = "tenders_responses"

    tender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tender.id"), primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), primary_key=True
    )
    price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    respond_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.current_timestamp()
    )

    tender = relationship("Tender", back_populates="tender_respond")
    user = relationship("User", back_populates="tender_respond")
