from typing import List, Optional

from fastapi import Depends
from repositories.postgres import (
    TenderRepository,
    UserRepository,
    VerificationRepository,
)
from repositories.postgres.schemas import VerificationRequest
from repositories.typesense import TenderIndex
from schemas import models


class ManagerService:
    user_repository: UserRepository
    tender_repository: TenderRepository
    tender_index: TenderIndex
    verf_repository: VerificationRepository

    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        tender_repository: TenderRepository = Depends(),
        tender_index: TenderIndex = Depends(),
        verf_repository: VerificationRepository = Depends(),
    ) -> None:
        self.user_repository = user_repository
        self.tender_repository = tender_repository
        self.tender_index = tender_index
        self.verf_repository = verf_repository

    async def response_user_verification_request(
        self, user_id: str, status: bool, verf_id: str, msg: Optional[str]
    ) -> None:
        await self.verf_repository.response_verification_requests(
            verf_id=verf_id, is_verified=status, msg=msg
        )
        await self.user_repository.update_verified_status(
            user_id=user_id, verified=status
        )

    async def get_verfication_request(
        self, verf_id: str
    ) -> VerificationRequest:
        return await self.verf_repository.get_verf_by_id(verf_id=verf_id)

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
        self.tender_index.update_verified_status(
            tender_id=tender_id, verified=status
        )
