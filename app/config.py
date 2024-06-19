import os
import tomllib

from dotenv import load_dotenv

load_dotenv()


class Config:
    class Database:
        class Postgres:
            DB_DSN: str = os.getenv(
                "DB_DSN",
                "postgresql+asyncpg://postgres:12345@localhost:5432/postgres",
            )

        class Typesense:
            API_KEY: str = os.getenv("TYPESENSE_API_KEY", "xyz")
            HOST: str = os.getenv("TYPESENSE_HOST", "localhost")
            PORT: str = os.getenv("TYPESENSE_PORT", "8108")
            PROTOCOL: str = os.getenv("TYPESENSE_PROTOCOL", "http")

        class Redis:
            DSN: str = os.getenv("REDIS_HOST", "redis://localhost")
            PASSWORD: str = os.getenv("REDIS_PASSWORD", "12345")

    class Broker:
        class JetStream:
            DSN: str = os.getenv("NATS_HOST", "nats://localhost:4222")

    class JWT:
        secret: str = os.getenv("JWT_SECRET", "secret")
        time_live: int = int(os.getenv("JWT_TTL", 20))

    class Session:
        time_live: int = int(os.getenv("SESSION_TTL", 336))

    class Role:
        super_admin = 1 << 7
        admin = 1 << 6
        manager = 1 << 5

        guest = 1 << 0

    class Dadata:
        api_key = os.getenv("DADATA_TOKEN", 336)

    class Localization:
        with open("localization.toml", "rb") as f:
            config = tomllib.load(f)


config = Config()


def get_config() -> Config:
    return config
