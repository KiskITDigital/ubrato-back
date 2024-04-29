from typing import List, Tuple

from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import (
    USER_EMAIL_NOT_FOUND,
    USERID_NOT_FOUND,
    RepositoryException,
)
from repositories.postgres.schemas import Organization, User
from schemas import models
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def create(
        self, user: User, org: Organization
    ) -> Tuple[models.User, models.Organization]:
        self.db.add(user)
        await self.db.flush()
        org.user_id = user.id
        self.db.add(org)
        await self.db.commit()

        await self.db.refresh(user)
        await self.db.refresh(org)

        return models.User(**user.__dict__), models.Organization(
            **org.__dict__
        )

    async def get_by_email(self, email: str) -> models.User:
        query = await self.db.execute(select(User).where(User.email == email))
        user = query.scalar()
        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USER_EMAIL_NOT_FOUND.format(email),
                sql_msg="",
            )

        return models.User(**user.__dict__)

    async def update_verified_status(
        self, user_id: str, verified: bool
    ) -> None:
        query = await self.db.execute(select(User).where(User.id == user_id))

        user = query.scalar()

        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USERID_NOT_FOUND.format(user_id),
                sql_msg="",
            )

        user.verified = verified
        await self.db.commit()

    async def get_all_users(
        self,
    ) -> List[models.User]:
        query = await self.db.execute(select(User))
        users: List[models.User] = []

        for user in query:
            users.append(models.User(**user.__dict__))

        return users

    async def get_by_id(self, user_id: str) -> models.User:
        query = await self.db.execute(select(User).where(User.id == user_id))

        users = query.scalar()

        if users is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USERID_NOT_FOUND.format(user_id),
                sql_msg="",
            )

        return models.User(**users.__dict__)

    async def update_avatar(self, user_id: str, avatar: str) -> None:
        query = await self.db.execute(select(User).where(User.id == user_id))

        user = query.scalar()

        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=USERID_NOT_FOUND.format(user_id),
                sql_msg="",
            )

        user.avatar = avatar
        await self.db.commit()

    async def update_password(self, email: str, password: str) -> None:
        await self.db.execute(
            update(User).where(User.email == email).values(password=password)
        )

        await self.db.commit()
