from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[int] = mapped_column(Integer, ForeignKey("document_types.id"))
    user_id: Mapped[str] = mapped_column(String(40), ForeignKey("users.id"))

    user = relationship("User", back_populates="documents")
    doc_type = relationship("DocumentType", back_populates="documents")


class DocumentType(Base):
    __tablename__ = "document_types"

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, cycle=True), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    documents = relationship("Document", back_populates="doc_type")
