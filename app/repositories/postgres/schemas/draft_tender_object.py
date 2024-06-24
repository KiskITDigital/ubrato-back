from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DraftTenderObjectType(Base):
    __tablename__ = "draft_tender_objects_types"

    tender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("draft_tender.id"), primary_key=True
    )
    object_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("objects_types.id"), primary_key=True
    )

    object_type = relationship(
        "ObjectType", back_populates="draft_object_group"
    )
    draft_tender = relationship(
        "DraftTender", back_populates="draft_tender_object_type"
    )
