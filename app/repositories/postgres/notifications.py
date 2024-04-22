from typing import List, Optional

from fastapi import Depends
from repositories.postgres.database import get_db_connection
from repositories.postgres.schemas import Notification
from schemas import models
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class NotificationRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def add_notice(
        self,
        user_id: str,
        header: Optional[str],
        msg: Optional[str],
        href: Optional[str],
        href_text: Optional[str],
        href_color: Optional[int],
    ) -> None:
        self.db.add(
            Notification(
                user_id=user_id,
                header=header,
                msg=msg,
                href=href,
                href_text=href_text,
                href_color=href_color,
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

    async def mark_read(self, ids: List[int], user_id: str) -> None:
        query = await self.db.execute(
            select(Notification).where(
                and_(Notification.user_id == user_id, Notification.id.in_(ids))
            )
        )

        for notice in query.scalars():
            notice.read = True

        await self.db.commit()
