from datetime import datetime
from typing import List

from repositories.postgres.schemas.base import Base
from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Questionnaire(Base):
    __tablename__ = "questionnaire"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    answers: Mapped[List[str]] = mapped_column(ARRAY(Text))
    user_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )

    user = relationship("User", back_populates="questionnaire")
