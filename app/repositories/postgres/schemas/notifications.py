from typing import Tuple

from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Notification(Base):
    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), primary_key=True
    )
    msg: Mapped[str] = mapped_column(String)
    href: Mapped[Tuple[str, None]] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="notification")
