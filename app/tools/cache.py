import pickle
from functools import wraps
from typing import Any, Awaitable, Callable, Optional

from repositories import redis


# TODO: подмумать о том как убрать костыль key. Сейчас он связан с тем
# что каждый раз генерируется сессия в get_db и классы генерится заново :(
def redis_cache(
    ttl: int = 3600,
    key: Optional[str] = None,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    def decorator(
        func: Callable[..., Awaitable[Any]]
    ) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            redis_client = redis.get_db_connection()
            hash_key = key if key else f"{func.__name__}:{args}:{kwargs}"
            cached_result = await redis_client.get(hash_key)
            if cached_result is not None:
                return pickle.loads(cached_result)
            result = await func(*args, **kwargs)
            await redis_client.set(
                hash_key, pickle.dumps(result, protocol=0), ex=ttl
            )
            return result

        return wrapper

    return decorator
