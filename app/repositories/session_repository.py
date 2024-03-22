from typing import Optional, Tuple

from fastapi import Depends
from repositories.database import get_db_connection
from repositories.exceptions import SESSION_NOT_FOUND
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
            return None
        except SQLAlchemyError as err:
            return None, Exception(err.code)

    def get_by_id(
        self, session_id: str
    ) -> Tuple[Optional[Session], Optional[Exception]]:
        try:
            session = self.db.query(Session).filter_by(id=session_id).first()

            if session:
                return session, None

            return Session, Exception(SESSION_NOT_FOUND)
        except SQLAlchemyError as err:
            self.db.rollback()
            return Session, Exception(err.code)
