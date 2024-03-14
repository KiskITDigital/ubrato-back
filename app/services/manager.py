from typing import List, Optional, Tuple

import models
from fastapi import Depends
from repositories import UserRepository


class ManagerService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self.user_repository = user_repository

    def update_verify_status(
        self, user_id: str, status: bool
    ) -> Optional[Exception]:
        return self.user_repository.update_verify_status(user_id, status)

    def get_all_users(self) -> Tuple[List[models.User], Optional[Exception]]:
        return self.user_repository.get_all_users()

    def get_by_id(
        self, user_id: str
    ) -> Tuple[models.User, Optional[Exception]]:
        return self.user_repository.get_by_id(user_id=user_id)
