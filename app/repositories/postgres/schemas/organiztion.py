from datetime import datetime
from typing import List, Optional

from repositories.postgres.schemas.base import Base
from schemas import models
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    brand_name: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(50), nullable=False)
    inn: Mapped[str] = mapped_column(String(10), nullable=False)
    okpo: Mapped[str] = mapped_column(String(8), nullable=False)
    ogrn: Mapped[str] = mapped_column(String(15), nullable=False)
    kpp: Mapped[str] = mapped_column(String(12), nullable=False)
    tax_code: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[List[dict[str, str]]] = mapped_column(
        JSONB, default=[], nullable=True
    )
    phone: Mapped[List[dict[str, str]]] = mapped_column(
        JSONB, default=[], nullable=True
    )
    messenger: Mapped[List[dict[str, str]]] = mapped_column(
        JSONB, default=[], nullable=True
    )
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
    customer_profile = relationship("CustomerProfile", back_populates="org")
    customer_locations = relationship("CustomerLocation", back_populates="org")
    contractor_profile = relationship(
        "ContractorProfile", back_populates="org"
    )
    contractor_services = relationship(
        "ContractorService", back_populates="org"
    )
    contractor_objects = relationship("ContractorObject", back_populates="org")
    contractor_cv = relationship("ContractorCV", back_populates="org")
    contractor_locations = relationship(
        "ContractorLocation", back_populates="org"
    )

    def to_model(self) -> models.Organization:
        email: List[models.ContactInfo] = []
        for info in self.email:
            email.append(
                models.ContactInfo(
                    contact=info["contact"], info=info["description"]
                )
            )

        phone: List[models.ContactInfo] = []
        for info in self.phone:
            phone.append(
                models.ContactInfo(
                    contact=info["contact"], info=info["description"]
                )
            )

        messenger: List[models.ContactInfo] = []
        for info in self.messenger:
            messenger.append(
                models.ContactInfo(
                    contact=info["contact"], info=info["description"]
                )
            )

        return models.Organization(
            id=self.id,
            brand_name=self.brand_name,
            full_name=self.full_name,
            short_name=self.short_name,
            inn=self.inn,
            okpo=self.okpo,
            ogrn=self.ogrn,
            kpp=self.kpp,
            tax_code=self.tax_code,
            address=self.address,
            avatar=self.avatar,
            email=email,
            phone=phone,
            messenger=messenger,
            user_id=self.user_id,
            update_at=self.update_at,
            created_at=self.created_at,
        )
