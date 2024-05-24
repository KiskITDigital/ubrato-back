from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class UserFavoriteContractor(Base):
    __tablename__ = "user_favorite_contractor"

    contractor_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("organizations.id"), primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), primary_key=True
    )
