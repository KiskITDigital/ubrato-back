class JWTUser:
    id: str
    first_name: str
    middle_name: str
    last_name: str
    role: int
    verify: bool
    exp: int

    def __init__(
        self,
        id: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        role: int,
        verify: bool,
        exp: int,
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.role = role
        self.verify = verify
        self.exp = exp
