from config import Config, get_config
from redis import asyncio as aioredis

config: Config = get_config()

redis: aioredis.Redis = aioredis.from_url(
    config.Database.Redis.DSN, password=config.Database.Redis.PASSWORD
)


def get_db_connection() -> aioredis.Redis:
    return redis
