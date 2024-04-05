from datetime import datetime

from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import ORG_NOT_FOUND, RepositoryException
from repositories.postgres.schemas import Document, Organization
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

    def get_organization_by_id(
        self,
        org_id: str,
    ) -> Organization:
        org = (
            self.db.query(Organization)
            .filter(Organization.id == org_id)
            .first()
        )
        if org is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ORG_NOT_FOUND,
                sql_msg="",
            )
        return org

    def get_organization_by_user_id(
        self,
        user_id: str,
    ) -> Organization:
        org = (
            self.db.query(Organization)
            .filter(Organization.user_id == user_id)
            .first()
        )
        if org is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ORG_NOT_FOUND,
                sql_msg="",
            )
        return org

    def update_org(
        self,
        upd_org: Organization,
    ) -> Organization:
        org = (
            self.db.query(Organization)
            .filter(Organization.id == upd_org.id)
            .first()
        )
        if org is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ORG_NOT_FOUND,
                sql_msg="",
            )
        org.brand_name = upd_org.brand_name
        org.short_name = upd_org.short_name
        org.address = upd_org.address
        org.update_at = datetime.now()

        self.db.commit()
        self.db.refresh(org)

        return org
