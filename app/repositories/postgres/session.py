from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import (
    SESSION_NOT_FOUND,
    RepositoryException,
)
from repositories.postgres.schemas import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SessionRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def create(self, session: Session) -> None:
        self.db.add(session)
        await self.db.commit()

    async def get_by_id(self, session_id: str) -> Session:
        query = await self.db.execute(
            select(Session).where(Session.id == session_id)
        )

        session = query.scalar()

        if session is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=SESSION_NOT_FOUND,
                sql_msg="",
            )
        return session
