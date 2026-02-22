from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class OrderCreatedEvent:
    """Событие: Заказ создан (для отправки в RabbitMQ)"""
    order_id: str
    event_type: str = "order.created"
    timestamp: datetime | None = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now(UTC)


@dataclass
class OrderStatusChangedEvent:
    """Событие: Статус заказа изменен"""

    order_id: str
    old_status: str
    new_status: str
    event_type: str = "order.status_changed"
    timestamp: datetime | None = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now(UTC)
