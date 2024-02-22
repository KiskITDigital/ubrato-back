from typing import Optional

from fastapi import Depends
from repositories.user_repository import UserRepository


class ManagerService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self.user_repository = user_repository

    def update_verify_status(
        self, user_id: str, status: bool
    ) -> Optional[Exception]:
        return self.user_repository.update_verify_status(user_id, status)
