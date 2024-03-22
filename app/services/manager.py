from typing import List, Optional, Tuple

import models
from fastapi import Depends
from repositories import TenderRepository, UserRepository


class ManagerService:
    user_repository: UserRepository
    tender_repository: TenderRepository

    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self.user_repository = user_repository

    def update_user_verified_status(
        self, user_id: str, status: bool
    ) -> Optional[Exception]:
        return self.user_repository.update_verified_status(user_id, status)

    def get_all_users(
        self,
    ) -> Tuple[List[models.UserPrivateDTO], Optional[Exception]]:
        users, err = self.user_repository.get_all_users()

        if err is not None:
            return [], err

        usersDTO: List[models.UserPrivateDTO] = []
        for user in users:
            usersDTO.append(models.UserPrivateDTO(**user.__dict__))

        return usersDTO, None

    def get_by_id(
        self, user_id: str
    ) -> Tuple[models.UserPrivateDTO, Optional[Exception]]:
        user, err = self.user_repository.get_by_id(user_id=user_id)

        if err is not None:
            return models.UserPrivateDTO, err

        return user, None

    def update_tender_verified_status(
        self, tender_id: str, status: bool
    ) -> Optional[Exception]:
        err = self.tender_repository.update_verified_status(
            tender_id=tender_id, status=status
        )
        if err is not None:
            return err
        return self.tender_repository.update_active_status(
            tender_id=tender_id, active=status
        )
