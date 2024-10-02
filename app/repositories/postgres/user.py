from typing import List, Tuple

from config import get_config
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import RepositoryException
from repositories.postgres.schemas import (
    ContractorProfile,
    CustomerProfile,
    Organization,
    User,
    UserFavoriteContractor,
)
from schemas import models
from sqlalchemy import and_, delete, select, update
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

        self.db.add(CustomerProfile(org_id=org.id))
        await self.db.flush()
        if user.is_contractor:
            self.db.add(ContractorProfile(org_id=org.id))

        await self.db.commit()

        await self.db.refresh(user)
        await self.db.refresh(org)

        return models.User(**user.__dict__), org.to_model()

    async def get_by_email(self, email: str) -> models.User:
        query = await self.db.execute(select(User).where(User.email == email))
        user = query.scalar()
        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["user_email_not_found"]
                .format(email),
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
                detail=get_config()
                .Localization.config["errors"]["userid_not_found"]
                .format(user_id),
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
                detail=get_config()
                .Localization.config["errors"]["userid_not_found"]
                .format(user_id),
                sql_msg="",
            )

        return models.User(**users.__dict__)

    async def update_avatar(self, user_id: str, avatar: str) -> None:
        query = await self.db.execute(select(User).where(User.id == user_id))

        user = query.scalar()

        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["userid_not_found"]
                .format(user_id),
                sql_msg="",
            )

        user.avatar = avatar
        await self.db.commit()

    async def update_password(self, email: str, password: str) -> None:
        await self.db.execute(
            update(User).where(User.email == email).values(password=password)
        )

        await self.db.commit()

    async def add_favorite_contratctor(
        self, user_id: str, contractor_id: str
    ) -> None:
        self.db.add(
            UserFavoriteContractor(
                user_id=user_id, contractor_id=contractor_id
            )
        )
        await self.db.commit()

    async def remove_favorite_contratctor(
        self, user_id: str, contractor_id: str
    ) -> None:
        await self.db.execute(
            delete(UserFavoriteContractor).where(
                and_(
                    UserFavoriteContractor.user_id == user_id,
                    UserFavoriteContractor.contractor_id == contractor_id,
                )
            )
        )

        await self.db.commit()

    async def is_favorite_contratctor(
        self, user_id: str, contractor_id: str
    ) -> bool:
        query = await self.db.execute(
            select(UserFavoriteContractor).where(
                and_(
                    UserFavoriteContractor.user_id == user_id,
                    UserFavoriteContractor.contractor_id == contractor_id,
                )
            )
        )

        return query.scalar() is not None

    async def get_favorite_contratctor(
        self, user_id: str
    ) -> List[models.FavoriteContractor]:
        query = await self.db.execute(
            select(
                UserFavoriteContractor.contractor_id, Organization.brand_name
            )
            .join(
                Organization,
                Organization.id == UserFavoriteContractor.contractor_id,
            )
            .where(UserFavoriteContractor.user_id == user_id)
        )

        contractors: List[models.FavoriteContractor] = []

        for contractor in query.all():
            id, name = contractor.tuple()
            contractors.append(
                models.FavoriteContractor(
                    id=id,
                    org_name=name,
                )
            )

        return contractors

    async def set_email_verified_status(
        self, user_id: str, verified: bool
    ) -> None:
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(email_verified=verified)
        )
        await self.db.commit()

    async def update_info(
        self,
        user_id: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        phone: str,
    ) -> None:
        query = await self.db.execute(select(User).where(User.id == user_id))

        user = query.scalar()

        if user is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["userid_not_found"]
                .format(user_id),
                sql_msg="",
            )

        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.phone = phone
        await self.db.commit()
