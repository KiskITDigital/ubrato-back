from fastapi import Depends, status
from repositories.database import get_db_connection
from repositories.exceptions import RepositoryException
from repositories.schemas import Document, Organization
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session


class OrganizationRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def save_organization(
        self,
        org: Organization,
    ) -> None:
        try:
            self.db.add(org)
            self.db.commit()
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err.code,
                sql_msg=err._message(),
            )

    def save_docs(
        self,
        document: Document,
    ) -> None:
        try:
            self.db.add(document)
            self.db.commit()
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err.code,
                sql_msg=err._message(),
            )
