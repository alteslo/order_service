import json
from typing import Any

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractRobustConnection

from src.core.config import settings


class EventPublisher:
    def __init__(self) -> None:
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._exchange: AbstractExchange | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(settings.rabbitmq_url)
        self._channel = await self._connection.channel()

        self._exchange = await self._channel.declare_exchange(
            "orders_events", aio_pika.ExchangeType.TOPIC, durable=True
        )

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()

    async def publish(self, routing_key: str, message: Any) -> None:
        """Публикация события в очередь"""
        if not self._exchange:
            raise RuntimeError("EventPublisher not connected")

        body = json.dumps(message, default=str).encode()
        message_obj = aio_pika.Message(
            body=body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self._exchange.publish(message_obj, routing_key)

    async def publish_order_created(self, order_id: str, user_id: str) -> None:
        """Публикация события создания заказа"""
        await self.publish(
            "order.created",
            {
                "event_type": "new_order",
                "order_id": order_id,
                "user_id": user_id,
            },
        )

event_publisher = EventPublisher()  # Глобальный экземпляр публишера


async def get_event_publisher() -> EventPublisher:
    """Зависимость для получения публишера"""
    return event_publisher
