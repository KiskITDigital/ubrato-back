import datetime
from datetime import timezone

import jwt
import models
from config import Config, get_config
from fastapi import Depends, status
from schemas.jwt_user import JWTUser
from services.exceptions import (
    INVALID_BARRIER,
    NO_BARRIER_TOKEN,
    AuthException,
    ServiceException,
)


class JWTService:
    secret: str
    time_live: int
    algorithm: str

    def __init__(self, config: Config = Depends(get_config)) -> None:
        self.secret = config.JWT.secret
        self.time_live = int(config.JWT.time_live)
        self.algorithm = "HS256"

    def generate_jwt(self, user: models.User) -> str:
        exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(
            minutes=self.time_live
        )

        jwt_user = JWTUser(
            user.id,
            user.first_name,
            user.middle_name,
            user.last_name,
            user.role,
            user.verified,
            int(exp.timestamp()),
        )

        encoded_data = jwt.encode(
            vars(jwt_user), key=self.secret, algorithm=self.algorithm
        )

        return encoded_data

    def decode_jwt(self, token: str) -> JWTUser:
        try:
            userd_dict = jwt.decode(
                token, self.secret, algorithms=self.algorithm
            )

            jwt_user = JWTUser(**userd_dict)

            return jwt_user
        except Exception:
            raise ServiceException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=INVALID_BARRIER,
            )

    def unmarshal_jwt(self, authorization: str) -> JWTUser:
        header = authorization.split(" ", 1)
        if header[0] != "Bearer":
            raise AuthException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=NO_BARRIER_TOKEN,
            )

        return self.decode_jwt(header[1])
