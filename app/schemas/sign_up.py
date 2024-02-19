from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from repositories import user_schema


PhoneNumber.phone_format = "E164"


class SignUpSchema(BaseModel):
    brand_name: str
    inn: int
    email: EmailStr
    phone: PhoneNumber
    password: str
    first_name: str
    middle_name: str
    last_name: str

    def to_shema(self) -> user_schema.User:
        return user_schema.User(
            brand_name=self.brand_name,
            inn=self.inn,
            email=self.email,
            phone=self.phone,
            password=self.password,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
        )
