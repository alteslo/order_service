import re
from dataclasses import dataclass
from enum import Enum


# TODO Можно провести рефакторинг и вынести в отдельные файлы, если количество Value Object будет расти

class OrderStatus(str, Enum):
    """Статусы заказа"""
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELED = "canceled"
    # CONFIRMED = "confirmed"
    # DELIVERED = "delivered"

    @classmethod
    def can_transition_to(cls, from_status: OrderStatus, to_status: OrderStatus) -> bool:
        """
        Бизнес-правило: валидация перехода между статусами.
        Запрещаем недопустимые изменения состояний.

        :param from_status: Cтартовый статус заказа
        :type from_status: OrderStatus
        :param to_status: Новый статус заказа
        :type to_status: OrderStatus
        :return: True, если переход допустим, иначе False
        :rtype: bool
        """
        allowed_transitions = {
            OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELED},
            OrderStatus.PAID: {OrderStatus.SHIPPED, OrderStatus.CANCELED},
            OrderStatus.SHIPPED: set(),
            OrderStatus.CANCELED: set(),
        }
        return to_status in allowed_transitions[from_status]


@dataclass(frozen=True)
class Email(str):
    """
    Value Object для email.
    Гарантирует валидацию формата при создании.
    """
    value: str

    def __post_init__(self):
        if not self._is_valid(self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    @staticmethod
    def _is_valid(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None


@dataclass(frozen=True)
class Money:
    """
    Value Object для денежных сумм.
    Гарантирует, что сумма не может быть отрицательной.
    """
    amount: float

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

    def __add__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.amount + other.amount)


__all__ = ["OrderStatus", "Email", "Money"]
