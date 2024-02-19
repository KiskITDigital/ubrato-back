from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from configs.config import Config

config = Config()

print(config.DB_DSN)
engine = create_engine(config.DB_DSN)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_connection() -> Generator[scoped_session, None, None]:
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
