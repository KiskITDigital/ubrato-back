from typing import Generator

from config import Config, get_config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

config: Config = get_config()

engine = create_engine(config.Database.DB_DSN, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_connection() -> Generator[scoped_session, None, None]:  # type: ignore
    db: scoped_session[Session] = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.remove()
