import datetime
from datetime import timezone

import jwt
from config import Config, get_config
from fastapi import Depends, status
from schemas import models
from schemas.jwt_user import JWTAuthUser, JWTUser
from services.exceptions import AuthException, ServiceException


class JWTService:
    secret: str
    time_live: int
    algorithm: str

    def __init__(self, config: Config = Depends(get_config)) -> None:
        self.localization = get_config().Localization.config
        self.secret = config.JWT.secret
        self.time_live = int(config.JWT.time_live)
        self.algorithm = "HS256"

    def generate_jwt(self, user: models.User, org: models.Organization) -> str:
        exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(
            minutes=self.time_live
        )

        jwt_user = JWTUser(
            id=user.id,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            role=user.role,
            verified=user.verified,
            is_contractor=user.is_contractor,
            org_id=org.id,
            org_short_name=org.short_name,
            org_inn=org.inn,
            org_okpo=org.okpo,
            org_ogrn=org.ogrn,
            org_kpp=org.kpp,
            exp=int(exp.timestamp()),
        )

        encoded_data = jwt.encode(
            vars(jwt_user), key=self.secret, algorithm=self.algorithm
        )

        return encoded_data

    def decode_jwt(self, token: str) -> JWTUser:
        try:
            userd_dict = jwt.decode(
                token, self.secret, algorithms=[self.algorithm]
            )

            jwt_user = JWTUser(**userd_dict)

            return jwt_user
        except Exception:
            raise ServiceException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.localization["errors"]["invalid_barrier"],
            )

    def unmarshal_jwt(self, authorization: str) -> JWTUser:
        header = authorization.split(" ", 1)
        if header[0] != "Bearer":
            raise AuthException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=self.localization["errors"]["no_barrier_token"],
            )

        return self.decode_jwt(header[1])

    def generate_auth_jwt(self, user_id: str) -> str:
        exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(
            hours=24
        )

        jwt_user = JWTAuthUser(
            id=user_id,
            exp=int(exp.timestamp()),
        )

        encoded_data = jwt.encode(
            vars(jwt_user), key=self.secret, algorithm=self.algorithm
        )

        return encoded_data

    def decode_auth_jwt(self, token: str) -> JWTAuthUser:
        try:
            userd_dict = jwt.decode(
                token, self.secret, algorithms=[self.algorithm]
            )

            jwt_user = JWTAuthUser(**userd_dict)

            return jwt_user
        except Exception:
            raise ServiceException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.localization["errors"]["invalid_barrier"],
            )
