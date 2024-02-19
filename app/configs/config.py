import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_DSN: str = os.getenv("DB_DNS")
