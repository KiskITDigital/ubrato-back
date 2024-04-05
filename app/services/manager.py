from typing import List

import models
from fastapi import Depends
from repositories.postgres import TenderRepository, UserRepository


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

    def update_user_verified_status(self, user_id: str, status: bool) -> None:
        self.user_repository.update_verified_status(
            user_id=user_id, verified=status
        )

    def get_all_users(
        self,
    ) -> List[models.UserPrivateDTO]:
        users = self.user_repository.get_all_users()

        usersDTO: List[models.UserPrivateDTO] = []
        for user in users:
            usersDTO.append(models.UserPrivateDTO(**user.__dict__))

        return usersDTO

    def get_user_by_id(self, user_id: str) -> models.UserPrivateDTO:
        user = self.user_repository.get_by_id(user_id=user_id)

        return models.UserPrivateDTO(**user.__dict__)

    def update_tender_verified_status(
        self, tender_id: int, status: bool
    ) -> None:
        self.tender_repository.update_verified_status(
            tender_id=tender_id, verified=status
        )
