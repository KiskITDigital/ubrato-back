from datetime import datetime
from typing import List

from repositories.postgres.schemas.base import Base
from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DraftTender(Base):
    __tablename__ = "draft_tender"

    id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), primary_key=True
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
    update_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )

    user = relationship("User", back_populates="draft_tender")
    city = relationship("City")
    draft_tender_service_type = relationship(
        "DraftTenderServiceType", back_populates="draft_tender"
    )
    draft_tender_object_type = relationship(
        "DraftTenderObjectType", back_populates="draft_tender"
    )
