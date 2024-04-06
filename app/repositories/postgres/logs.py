from fastapi import Depends
from repositories.postgres.database import get_db_connection
from repositories.postgres.schemas import Logs
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class LogsRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def save(self, logs: Logs) -> None:
        try:
            self.db.add(logs)
            await self.db.commit()
        except SQLAlchemyError as err:
            print(err._message())
