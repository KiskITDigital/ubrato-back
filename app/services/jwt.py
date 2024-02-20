import datetime
from datetime import timezone
from typing import Self

import jwt
from config import Config
from models.user_model import User
from schemas.jwt_user import JWTUser

config = Config()


class JWTService:
    secret: str
    time_live: int

    def __init__(self) -> Self:
        self.secret = config.JWT.secret
        self.time_live = int(config.JWT.time_live)

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
