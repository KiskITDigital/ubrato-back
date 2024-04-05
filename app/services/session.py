import datetime
import secrets

import models
from config import Config, get_config
from fastapi import Depends, status
from repositories.postgres import SessionRepository, UserRepository
from repositories.postgres.schemas import Session
from services.exceptions import SESSION_EXPIRED, ServiceException


class SessionService:
    session_repository: SessionRepository
    user_repository: UserRepository
    time_live: int

    def __init__(
        self,
        config: Config = Depends(get_config),
        user_repository: UserRepository = Depends(),
        session_repository: SessionRepository = Depends(),
    ) -> None:
        self.time_live = int(config.Session.time_live)
        self.session_repository = session_repository
        self.user_repository = user_repository
        return

    def create_session(self, user_id: str) -> str:
        session_id = secrets.token_hex(32 // 2)
        expires_at = datetime.datetime.now() + datetime.timedelta(
            hours=self.time_live
        )
        self.session_repository.create(
            session=Session(
                id=session_id, user_id=user_id, expires_at=expires_at
            )
        )
        return session_id

    def get_user_session_by_id(self, session_id: str) -> models.User:
        session = self.session_repository.get_by_id(session_id=session_id)

        if (
            session.expires_at.timestamp()
            < datetime.datetime.now().timestamp()
        ):
            raise ServiceException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=SESSION_EXPIRED,
            )

        user = self.user_repository.get_by_id(user_id=session.user_id)

        return user
