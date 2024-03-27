from fastapi import Depends
from repositories.database import get_db_connection
from repositories.schemas import Logs
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session


class LogsRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def save(self, logs: Logs) -> None:
        try:
            self.db.add(logs)
            self.db.commit()
        except SQLAlchemyError as err:
            print(err._message())
