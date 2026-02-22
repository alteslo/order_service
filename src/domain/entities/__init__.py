import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from src.domain.events import OrderCreatedEvent
from src.domain.value_objects import Email, Money, OrderStatus


# TODO Можно провести рефакторинг и вынести в отдельные файлы, если количество Value Object будет расти


@dataclass
class User:
    """Сущность пользователя."""

    email: Email
    password_hash: str

    id: UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, email: str, password_hash: str) -> User:
        """
        Фабричный метод для создания нового пользователя.
        Гарантирует, что email будет валидирован через Value Object.

        :param email: Адрес электронной почты пользователя
        :type email: str
        :param password_hash: Хэш пароля пользователя
        :type password_hash: str
        :return: Новый экземпляр User
        :rtype: User
        """
        return cls(email=Email(email), password_hash=password_hash, id=uuid.uuid4())


@dataclass
class Order:
    user_id: UUID
    items: list[str]
    tottal_price: Money
    status: OrderStatus = OrderStatus.PENDING

    id: UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    # Список доменных событий, не сохраняется в БД
    _domain_events: list[str] = field(default_factory=list, init=False, repr=False)

    @classmethod
    def create(cls, user_id: UUID, items: list[str], tottal_price: Money) -> Order:
        """
        Фабричный метод для создания нового заказа.
        Гарантирует, что статус заказа будет установлен в PENDING по умолчанию.

        :param user_id: Идентификатор пользователя, который создает заказ
        :type user_id: UUID
        :param items: Список наименований товаров в заказе
        :type items: list[str]
        :param tottal_price: Общая стоимость заказа
        :type tottal_price: Money
        :return: Новый экземпляр Order
        :rtype: Order
        """
        order = cls(
            user_id=user_id, items=items, tottal_price=tottal_price, status=OrderStatus.PENDING, id=uuid.uuid4()
        )

        order._add_domain_event(OrderCreatedEvent(order_id=str(order.id)))

        return order

    def change_status(self, new_status: OrderStatus) -> None:
        """
        Метод для изменения статуса заказа.
        Включает бизнес-правило валидации переходов между статусами.

        :param new_status: Новый статус заказа
        :type new_status: OrderStatus
        :raises ValueError: Если переход между статусами недопустим
        """
        if not OrderStatus.can_transition_to(self.status, new_status):
            raise ValueError(f"Invalid status transition from {self.status} to {new_status}")

        self.status = new_status

    def get_domain_events(self) -> list:
        """
        Получить список доменных событий, связанных с этим заказом.

        :return: Список доменных событий
        :rtype: list
        """
        return self._domain_events

    def clear_domain_events(self) -> None:
        """
        Очистить список доменных событий после их обработки.
        """
        self._domain_events.clear()

    def _add_domain_event(self, event) -> None:
        self._domain_events.append(event)


class DomainException(Exception):
    """Базовое исключение доменного слоя"""

    pass


class InvalidStatusTransitionError(DomainException):
    """Попытка недопустимого перехода статуса"""

    pass
