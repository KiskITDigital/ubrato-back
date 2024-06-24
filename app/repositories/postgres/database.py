from typing import AsyncGenerator

from config import Config, get_config
from fastapi import status
from repositories.postgres.exceptions import RepositoryException
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

config: Config = get_config()

engine = create_async_engine(config.Database.Postgres.DB_DSN)
async_session_maker = async_sessionmaker(autocommit=False, bind=engine)


async def get_db_connection() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            session.begin()
            yield session
        except OperationalError:
            await session.rollback()
            raise Exception("Can't access the database")
        except IntegrityError as err:
            await session.rollback()
            print(err._message())
            raise RepositoryException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=config.Localization.config["errors"][
                    "data_already_exist"
                ],
                sql_msg=err._message(),
            )
        except SQLAlchemyError as err:
            await session.rollback()
            print(err._sql_message())
            print(err._message())
            raise RepositoryException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err.code,
                sql_msg=err._message(),
            )

        finally:
            await session.close()
