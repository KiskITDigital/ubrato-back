from datetime import datetime
from typing import Optional

from repositories.postgres.schemas.base import Base
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(40), ForeignKey("users.id"))
    header: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    msg: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    href: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    href_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    href_color: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.current_timestamp()
    )

    user = relationship("User", back_populates="notification")
