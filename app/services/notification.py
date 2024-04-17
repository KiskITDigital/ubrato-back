from typing import Optional

from fastapi import Depends
from repositories.postgres import NotificationRepository
from schemas import models


class NoticeService:
    notification_repository: NotificationRepository

    def __init__(
        self,
        notification_repository: NotificationRepository = Depends(),
    ) -> None:
        self.notification_repository = notification_repository

    async def add_notice(
        self,
        user_id: str,
        header: Optional[str],
        msg: Optional[str],
        href: Optional[str],
    ) -> None:
        return await self.notification_repository.add_notice(
            user_id=user_id, header=header, msg=msg, href=href
        )

    async def get_user_notice(self, user_id: str) -> models.Notifications:
        notifications = await self.notification_repository.get_user_notice(
            user_id=user_id
        )

        return models.Notifications(
            total=len(notifications),
            notifications=notifications,
        )
