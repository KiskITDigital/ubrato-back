from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    brand_name = Column(String)
    inn = Column(Integer)
    email = Column(String)
    phone = Column(String)
    password = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=func.current_timestamp())
