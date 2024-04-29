import pickle
from functools import wraps
from hashlib import sha256
from typing import Any, Awaitable, Callable, List, Optional, Type

from repositories import redis


def redis_cache(
    ttl: int = 3600,
    key: Optional[str] = None,
    ignore_classes: Optional[List[Type[Any]]] = None,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    if ignore_classes is None:
        ignore_classes = []

    def decorator(
        func: Callable[..., Awaitable[Any]]
    ) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            redis_client = redis.get_db_connection()
            filtered_kwargs = {
                k: v
                for k, v in kwargs.items()
                if not any(isinstance(v, cls) for cls in ignore_classes)
            }
            hash_sum = sha256()
            for _, value in filtered_kwargs.items():
                hash_sum.update(str(value).encode())

            hash_key = (
                key if key else f"{func.__name__}:{hash_sum.hexdigest()}"
            )

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
