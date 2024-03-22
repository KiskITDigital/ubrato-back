import datetime
import secrets
from typing import Optional, Tuple

import models
from config import Config, get_config
from fastapi import Depends
from repositories import SessionRepository, UserRepository
from repositories.schemas import Session
from services.exceptions import SESSION_EXPIRED


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

    def create_session(self, user_id: str) -> Tuple[str, Optional[Exception]]:
        session_id = secrets.token_hex(32 // 2)
        expires_at = datetime.datetime.now() + datetime.timedelta(
            hours=self.time_live
        )
        err = self.session_repository.create(
            session=Session(
                id=session_id, user_id=user_id, expires_at=expires_at
            )
        )
        return session_id, err

    def get_user_session_by_id(
        self, session_id: str
    ) -> Tuple[models.User, Optional[Exception]]:
        session, err = self.session_repository.get_by_id(session_id=session_id)
        if err is not None:
            return models.User, err
        
        if session is None:
            return models.User, SESSION_EXPIRED

        if (
            session.expires_at.timestamp()
            < datetime.datetime.now().timestamp()
        ):
            return models.User, SESSION_EXPIRED

        user, err = self.user_repository.get_by_id(user_id=session.user_id)
        if err is not None:
            return models.User, err

        return user, None
