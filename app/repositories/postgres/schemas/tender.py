from datetime import datetime
from typing import List

from repositories.postgres.schemas.base import Base
from repositories.typesense.schemas import TypesenseTender
from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Tender(Base):
    __tablename__ = "tender"

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, cycle=True), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    is_contract_price: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_nds_price: Mapped[bool] = mapped_column(Boolean, nullable=False)
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cities.id"), nullable=False
    )
    floor_space: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(400))
    wishes: Mapped[str] = mapped_column(String(400))
    specification: Mapped[str] = mapped_column(String(400))
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
    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )
    verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    user = relationship("User", back_populates="tender")
    city = relationship("City")
    tender_respond = relationship("TenderRespond", back_populates="tender")
    tender_service_type = relationship(
        "TenderServiceType", back_populates="tender"
    )
    tender_object_type = relationship(
        "TenderObjectType", back_populates="tender"
    )

    def ConvertToIndexSchema(
        self,
    ) -> TypesenseTender:
        return TypesenseTender(
            id=str(self.id),
            name=self.name,
            price=self.price,
            is_contract_price=self.is_contract_price,
            is_nds_price=self.is_nds_price,
            city_id=str(self.city_id),
            floor_space=self.floor_space,
            description=self.description,
            wishes=self.wishes,
            reception_start=int(self.reception_start.timestamp()),
            reception_end=int(self.reception_end.timestamp()),
            work_start=int(self.work_start.timestamp()),
            work_end=int(self.work_end.timestamp()),
            user_id=self.user_id,
            verified=self.verified,
            created_at=int(self.created_at.timestamp()),
        )
