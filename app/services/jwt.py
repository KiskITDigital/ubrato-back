import datetime
from datetime import timezone
from typing import Self
from fastapi import Depends

import jwt
from config import Config
from models.user_model import User
from schemas.jwt_user import JWTUser


class JWTService:
    secret: str
    time_live: int

    def __init__(self, config: Config = Depends()) -> None:
        self.secret = config.JWT.secret
        self.time_live = int(config.JWT.time_live)
        return

    def generate_jwt(self, user: User) -> str:
        exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(
            hours=self.time_live
        )

        jwt_user = JWTUser(
            user.id,
            user.first_name,
            user.middle_name,
            user.last_name,
            user.role,
            exp,
        )

        encoded_data = jwt.encode(
            jwt_user.__dict__, key=self.secret, algorithm="HS256"
        )

        return encoded_data
