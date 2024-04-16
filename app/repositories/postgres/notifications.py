from typing import List, Optional

from fastapi import Depends
from repositories.postgres.database import get_db_connection
from repositories.postgres.schemas import Notification
from schemas import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class NotificationRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def add_notice(
        self, user_id: str, msg: str, href: Optional[str]
    ) -> None:
        self.db.add(
            Notification(
                user_id=user_id,
                msg=msg,
                href=href,
            )
        )

        await self.db.commit()

    async def get_user_notice(self, user_id: str) -> List[models.Notification]:
        query = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id)
        )

        notifications: List[models.Notification] = []
        for notice in query.scalars():
            notifications.append(models.Notification(**notice.__dict__))

        return notifications
