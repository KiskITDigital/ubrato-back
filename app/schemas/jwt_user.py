from datetime import datetime


class JWTUser:
    id: str
    first_name: str
    middle_name: str
    last_name: str
    role: int
    exp: float

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
        self.exp = exp.timestamp()
        
        return
