import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    class Database:
        DB_DSN: str = os.getenv("DB_DNS", "")

    class JWT:
        secret: str = os.getenv("JWT_SECRET", "secret")
        time_live: int = int(os.getenv("JWT_TIME_LIVE", 24))

    class Role:
        super_admin = 1 << 7
        admin = 1 << 6
        manager = 1 << 5

        guest = 1 << 0


config = Config()


def get_config() -> Config:
    return config
