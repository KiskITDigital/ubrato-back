from datetime import datetime

import models
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import ORG_NOT_FOUND, RepositoryException
from repositories.postgres.schemas import Document, Organization
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class OrganizationRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def save_organization(
        self,
        org: Organization,
    ) -> None:
        self.db.add(org)
        await self.db.commit()

    async def save_docs(
        self,
        document: Document,
    ) -> None:
        self.db.add(document)
        await self.db.commit()

    async def get_organization_by_id(
        self,
        org_id: str,
    ) -> Organization:
        query = await self.db.execute(
            select(Organization).where(Organization.id == org_id)
        )

        org = query.scalar()

        if org is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ORG_NOT_FOUND,
                sql_msg="",
            )
        return org

    async def get_organization_by_user_id(
        self,
        user_id: str,
    ) -> models.Organization:
        query = await self.db.execute(
            select(Organization).where(Organization.user_id == user_id)
        )

        org = query.fetchone()

        if org is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ORG_NOT_FOUND,
                sql_msg="",
            )
        return models.Organization(**org[0].__dict__)

    async def update_org(
        self,
        upd_org: Organization,
    ) -> Organization:
        query = await self.db.execute(
            select(Organization).where(Organization.id == upd_org.id)
        )

        org = query.scalar()

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

        await self.db.commit()
        await self.db.refresh(org)

        return org
