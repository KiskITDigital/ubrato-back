from datetime import datetime

from repositories.postgres.schemas import Base
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
