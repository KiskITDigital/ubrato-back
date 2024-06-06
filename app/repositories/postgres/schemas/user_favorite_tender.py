from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class UserFavoriteTender(Base):
    __tablename__ = "user_favorite_tender"

    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), primary_key=True
    )
    tender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tender.id"), primary_key=True
    )
