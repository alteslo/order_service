import json
from typing import Any

import redis.asyncio as redis

from src.core.config import settings


class RedisClient:
    def __init__(self) -> None:
        self._client: redis.Redis | None = None
        self._ttl: int = 300

    async def connect(self) -> None:
        self._client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def close(self) -> None:
        if self._client:
            await self._client.close()

    def get(self, key):
        if not self._client:
            return None
        value = self._client.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        if not self._client:
            return
        await self._client.setex(
            key,
            ttl or self._ttl,
            json.dumps(value),
        )

    async def delete(self, key: str) -> None:
        if not self._client:
            return
        await self._client.delete(key)

    def get_order_key(self, order_id: str) -> str:
        return f"order:{order_id}"


redis_client = RedisClient()  # Глобальный экземпляр RedisClient для использования в приложении


async def get_redis_client() -> RedisClient:
    if not redis_client._client:
        await redis_client.connect()
    return redis_client
