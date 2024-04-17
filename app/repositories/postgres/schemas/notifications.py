from typing import Tuple

from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id")
    )
    header: Mapped[str] = mapped_column(String, nullable=True)
    msg: Mapped[str] = mapped_column(String, nullable=True)
    href: Mapped[Tuple[str, None]] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="notification")
