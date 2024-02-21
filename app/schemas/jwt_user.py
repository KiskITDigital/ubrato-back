from datetime import datetime
from typing import Any


class JWTUser:
    id: str
    first_name: str
    middle_name: str
    last_name: str
    role: int
    exp: int

    def __init__(
        self,
        id: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        role: int,
        exp: datetime,
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.role = role
        self.exp = int(exp.timestamp())

    def to_payload(self) -> dict[str, Any]:
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'role': self.role,
            'exp': self.exp
        }
