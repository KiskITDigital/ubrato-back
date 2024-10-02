import uuid
from hashlib import md5
from typing import List, Tuple

import bcrypt
import pyotp
from broker.nats import NatsClient, get_nats_connection
from broker.topic import EMAIL_CONFIRMATION_TOPIC, EMAIL_RESET_PASS_TOPIC
from config import get_config
from fastapi import Depends, status
from repositories.postgres import TenderRepository, UserRepository
from repositories.postgres.schemas import Organization, User
from repositories.typesense import ContractorIndex
from repositories.typesense.schemas import TypesenseContractor
from schemas import models
from schemas.pb.models.v1.email_confirmation_pb2 import EmailConfirmation
from schemas.pb.models.v1.password_recovery_pb2 import PasswordRecovery
from services.exceptions import ServiceException


class UserService:
    user_repository: UserRepository
    tender_repository: TenderRepository
    nats_client: NatsClient
    contractor_index: ContractorIndex

    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        tender_repository: TenderRepository = Depends(),
        contractor_index: ContractorIndex = Depends(),
        nats_client: NatsClient = Depends(get_nats_connection),
    ) -> None:
        self.user_repository = user_repository
        self.tender_repository = tender_repository
        self.nats_client = nats_client
        self.contractor_index = contractor_index
        self.localization = get_config().Localization.config

    async def create(
        self,
        email: str,
        phone: str,
        password: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        is_contractor: bool,
        avatar: str,
        org: Organization,
    ) -> Tuple[models.User, models.Organization]:
        id = "usr_" + str(uuid.uuid4())

        password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        totp_salt = pyotp.random_base32()

        user = User(
            id=id,
            email=email,
            phone=phone,
            password=password,
            totp_salt=totp_salt,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            is_contractor=is_contractor,
            avatar=avatar,
        )

        created_user, created_org = await self.user_repository.create(
            user=user, org=org
        )

        if created_user.is_contractor:
            self.contractor_index.save(
                contractor=TypesenseContractor(
                    id=created_org.id,
                    name=created_org.brand_name,
                    inn=created_org.inn,
                ),
                cities=[],
                objects=[],
                services=[],
            )

        return created_user, created_org

    async def get_by_email(self, email: str) -> models.User:
        user = await self.user_repository.get_by_email(email)

        return user

    async def get_by_id(self, id: str) -> models.UserPrivateDTO:
        user = await self.user_repository.get_by_id(id)

        return models.UserPrivateDTO(**user.__dict__)

    def password_valid(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    async def upd_avatar(self, user_id: str, avatar: str) -> None:
        await self.user_repository.update_avatar(
            user_id=user_id, avatar=avatar
        )

    async def ask_reset_pass(self, email: str) -> None:
        user = await self.get_by_email(email=email)

        totp = pyotp.TOTP(user.totp_salt, interval=1800)

        salt = md5()
        salt.update(totp.now().encode())

        payload = PasswordRecovery(
            email=user.email, salt=salt.hexdigest(), name=user.first_name
        )

        await self.nats_client.pub(
            EMAIL_RESET_PASS_TOPIC, payload=payload.SerializeToString()
        )

    async def reset_password(
        self, email: str, password: str, code: str
    ) -> None:
        user = await self.get_by_email(email=email)

        totp = pyotp.TOTP(user.totp_salt, interval=1800)

        salt = md5()
        salt.update(totp.now().encode())

        if salt.hexdigest() != code:
            raise ServiceException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.localization["errors"]["expired_reset_code"],
            )

        password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        await self.user_repository.update_password(
            email=email, password=password
        )

    async def add_favorite_contratctor(
        self, user_id: str, contractor_id: str
    ) -> None:
        await self.user_repository.add_favorite_contratctor(
            user_id=user_id, contractor_id=contractor_id
        )

    async def remove_favorite_contratctor(
        self, user_id: str, contractor_id: str
    ) -> None:
        await self.user_repository.remove_favorite_contratctor(
            user_id=user_id, contractor_id=contractor_id
        )

    async def is_favorite_contratctor(
        self, user_id: str, contractor_id: str
    ) -> bool:
        return await self.user_repository.is_favorite_contratctor(
            user_id=user_id, contractor_id=contractor_id
        )

    async def list_favorite_contratctor(
        self, user_id: str
    ) -> List[models.FavoriteContractor]:
        return await self.user_repository.get_favorite_contratctor(
            user_id=user_id
        )

    async def list_favorite_tenders(self, user_id: str) -> List[models.Tender]:
        return await self.tender_repository.get_user_favorites(user_id=user_id)

    async def confirm_email(self, user_id: str) -> None:
        await self.user_repository.set_email_verified_status(
            user_id=user_id, verified=True
        )

    async def ask_confirm_email(self, user_email: str, salt: str) -> None:
        payload = EmailConfirmation(email=user_email, salt=salt)

        await self.nats_client.pub(
            EMAIL_CONFIRMATION_TOPIC, payload=payload.SerializeToString()
        )

    async def upd_info(
        self,
        user_id: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        phone: str,
    ) -> None:
        return await self.user_repository.update_info(
            user_id=user_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=phone,
        )
