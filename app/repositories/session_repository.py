from typing import Optional

from fastapi import Depends
from repositories.database import get_db_connection
from repositories.exceptions import SESSION_NOT_FOUND, RepositoryException
from repositories.schemas import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session


class SessionRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create(self, session: Session) -> Optional[Exception]:
        try:
            self.db.add(session)
            self.db.commit()
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def get_by_id(self, session_id: str) -> Session:
        try:
            session = self.db.query(Session).filter_by(id=session_id).first()

            if session is None:
                raise RepositoryException(
                    status_code=404, detail=SESSION_NOT_FOUND, sql_msg=""
                )
            return session
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )
