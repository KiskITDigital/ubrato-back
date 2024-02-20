import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    class Database:
        DB_DSN: str = os.getenv("DB_DNS")

    class JWT:
        secret: str = os.getenv("JWT_SECRET")
        time_live: int = os.getenv("JWT_TIME_LIVE")

    class Role:
        super_admin = 1 << 7
        admin = 1 << 6
        manager = 1 << 5
