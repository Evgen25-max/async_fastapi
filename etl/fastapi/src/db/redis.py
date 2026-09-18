from typing import Optional

from redis.asyncio import Redis

from core.config import config

redis: Optional[Redis] = None


def init_redis() -> None:
    """Инициализирует клиент."""
    global redis
    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSW,
    )


async def close_redis() -> None:
    """Закрывает клиент."""
    global redis
    if redis is not None:
        await redis.close()
        redis = None


def get_redis() -> Redis:
    """Возвращает клиент."""
    if redis is None:
        raise RuntimeError(
            'Redis не инициализирован. Вызовите init_redis() при старте.'
        )
    return redis
