class JWTUser:
    id: str
    first_name: str
    middle_name: str
    last_name: str
    role: int
    verified: bool
    is_contractor: bool
    org_id: str
    org_short_name: str
    org_inn: str
    org_okpo: str
    org_ogrn: str
    org_kpp: str
    exp: int

    def __init__(
        self,
        id: str,
        first_name: str,
        middle_name: str,
        last_name: str,
        role: int,
        verified: bool,
        is_contractor: bool,
        org_id: str,
        org_short_name: str,
        org_inn: str,
        org_okpo: str,
        org_ogrn: str,
        org_kpp: str,
        exp: int,
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.role = role
        self.verified = verified
        self.is_contractor = is_contractor
        self.org_id = org_id
        self.org_short_name = org_short_name
        self.org_inn = org_inn
        self.org_okpo = org_okpo
        self.org_ogrn = org_ogrn
        self.org_kpp = org_kpp
        self.exp = exp
