from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import (
    SESSION_NOT_FOUND,
    RepositoryException,
)
from repositories.postgres.schemas import Session
from sqlalchemy.orm import Session as SQLSession
from sqlalchemy.orm import scoped_session


class SessionRepository:
    db: scoped_session[SQLSession]

    def __init__(
        self, db: scoped_session[SQLSession] = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, session: Session) -> None:
        self.db.add(session)
        self.db.commit()

    def get_by_id(self, session_id: str) -> Session:
        session = self.db.query(Session).filter_by(id=session_id).first()

        if session is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=SESSION_NOT_FOUND,
                sql_msg="",
            )
        return session
