from fastapi import Depends
from repositories.database import get_db_connection
from repositories.schemas import Logs
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session


class LogsRepository:
    db: scoped_session[Session]

    def __init__(
        self, db: scoped_session[Session] = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def save(self, logs: Logs) -> None:
        try:
            self.db.add(logs)
            self.db.commit()
        except SQLAlchemyError as err:
            print("asd")
            print(err._message())
