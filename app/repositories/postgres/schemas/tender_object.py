from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ObjectGroup(Base):
    __tablename__ = "objects_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))

    object_type = relationship("ObjectType", back_populates="object_group")


class ObjectType(Base):
    __tablename__ = "objects_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    object_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("objects_groups.id")
    )

    object_group = relationship("ObjectGroup", back_populates="object_type")
    tender_object_type = relationship(
        "TenderObjectType", back_populates="tender_object_type"
    )
    draft_object_group = relationship(
        "DraftTenderObjectType", back_populates="object_type"
    )
    contractor_objects = relationship(
        "ContractorObject", back_populates="object_type"
    )


class TenderObjectType(Base):
    __tablename__ = "tender_objects_types"

    tender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tender.id"), primary_key=True
    )
    object_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("objects_types.id"), primary_key=True
    )

    tender_object_type = relationship(
        "ObjectType", back_populates="tender_object_type"
    )
    tender = relationship("Tender", back_populates="tender_object_type")
