from typing import Generator

from config import Config, get_config
from fastapi import status
from repositories.exceptions import DATA_ALREADY_EXIST, RepositoryException
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session, sessionmaker

config: Config = get_config()

engine = create_engine(config.Database.DB_DSN, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_connection() -> Generator[scoped_session[Session], None, None]:
    db: scoped_session[Session] = scoped_session(SessionLocal)
    try:
        yield db
    except OperationalError:
        db.rollback()
        raise Exception("Can't access the database")
    except IntegrityError:
        db.rollback()
        raise RepositoryException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=DATA_ALREADY_EXIST,
                sql_msg="",
            )
    except SQLAlchemyError as err:
        db.rollback()
        raise RepositoryException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err.code,
            sql_msg=err._message(),
        )

    finally:
        db.close()
