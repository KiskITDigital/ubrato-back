from fastapi import Depends
from repositories.database import get_db_connection
from repositories.schemas import Document, Organization
from sqlalchemy.orm import Session, scoped_session


class OrganizationRepository:
    db: scoped_session[Session]

    def __init__(
        self, db: scoped_session[Session] = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def save_organization(
        self,
        org: Organization,
    ) -> None:
        self.db.add(org)
        self.db.commit()

    def save_docs(
        self,
        document: Document,
    ) -> None:
        self.db.add(document)
        self.db.commit()
