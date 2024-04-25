from config import Config, get_config
from redis import asyncio as aioredis

config: Config = get_config()

redis: aioredis.Redis = aioredis.from_url(
    "redis://localhost", password=config.Database.Redis.PASSWORD
)


def get_db_connection() -> aioredis.Redis:
    return redis
