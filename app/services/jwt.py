import datetime
from datetime import timezone
from fastapi import Depends

import jwt
from config import Config, get_config
from models.user_model import User
from schemas.jwt_user import JWTUser


class JWTService():
    secret: str
    time_live: int
    algorithm: str

    def __init__(self, config: Config = Depends(get_config)) -> None:
        self.secret = config.JWT.secret
        self.time_live = int(config.JWT.time_live)
        self.algorithm = "HS256"
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
            jwt_user.to_payload(), key=self.secret, algorithm=self.algorithm
        )

        return encoded_data
    
    def decode_jwt(self, token: str) -> tuple[JWTUser, Exception]:
        try:
            return jwt.decode(token, self.secret, algorithms=self.algorithm), None
        except Exception as err:
            return JWTUser, err
        

    # def is_super_admin(self, role) -> bool:
    #     role >= self.