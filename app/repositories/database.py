from typing import Generator

from config import Config, get_config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

config: Config = get_config()

engine = create_engine(config.Database.DB_DSN)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_connection() -> Generator[scoped_session, None, None]:
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
