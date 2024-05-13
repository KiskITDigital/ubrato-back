from repositories.postgres.schemas.base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"))

    region = relationship("Region", back_populates="cities")
    tenders = relationship("Tender", back_populates="city")
    draft_tender = relationship("DraftTender", back_populates="city")
    customer_locations = relationship(
        "CustomerLocation", back_populates="city"
    )
    contractor_locations = relationship(
        "ContractorLocation", back_populates="city"
    )
