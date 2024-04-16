from typing import List

from fastapi import Depends
from repositories.postgres import TenderRepository, UserRepository
from schemas import models


class ManagerService:
    user_repository: UserRepository
    tender_repository: TenderRepository

    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        tender_repository: TenderRepository = Depends(),
    ) -> None:
        self.user_repository = user_repository
        self.tender_repository = tender_repository

    async def update_user_verified_status(
        self, user_id: str, status: bool
    ) -> None:
        await self.user_repository.update_verified_status(
            user_id=user_id, verified=status
        )

    async def get_all_users(
        self,
    ) -> List[models.UserPrivateDTO]:
        users = await self.user_repository.get_all_users()

        usersDTO: List[models.UserPrivateDTO] = []
        for user in users:
            usersDTO.append(models.UserPrivateDTO(**user.__dict__))

        return usersDTO

    async def get_user_by_id(self, user_id: str) -> models.UserPrivateDTO:
        user = await self.user_repository.get_by_id(user_id=user_id)

        return models.UserPrivateDTO(**user.__dict__)

    async def update_tender_verified_status(
        self, tender_id: int, status: bool
    ) -> None:
        await self.tender_repository.update_verified_status(
            tender_id=tender_id, verified=status
        )
