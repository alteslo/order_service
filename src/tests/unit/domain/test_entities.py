from uuid import UUID

import pytest

from src.domain.entities import InvalidStatusTransitionError, Money, Order, User
from src.domain.events import OrderCreatedEvent
from src.domain.value_objects import OrderStatus


class TestOrder:
    def test_create_order_generates_event(self) -> None:
        """Проверка: при создании заказа генерируется событие"""
        order = Order.create(
            user_id=UUID("abdc284f-34a2-4bbe-966b-013b834cf889"),
            items=[{"name": "item1", "price": 100.0}],
            total_price=Money(100.0),
        )

        events = order.get_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], OrderCreatedEvent)
        assert events[0].order_id == str(order.id)
        assert events[0].event_type == "order.created"

    def test_status_transition_valid(self):
        """Проверка: валидный переход статуса (PENDING -> PAID)"""
        order = Order.create(user_id=UUID("abdc284f-34a2-4bbe-966b-013b834cf889"), items=[], total_price=Money(0))
        order.change_status(OrderStatus.PAID)
        assert order.status == OrderStatus.PAID

    def test_status_transition_invalid(self):
        """Проверка: недопустимый переход статуса (PENDING -> SHIPPED)"""
        order = Order.create(user_id=UUID("abdc284f-34a2-4bbe-966b-013b834cf889"), items=[], total_price=Money(0))
        with pytest.raises(InvalidStatusTransitionError):
            order.change_status(OrderStatus.SHIPPED)

    def test_negative_price_rejected(self):
        """Проверка: отрицательная цена отклоняется на уровне Value Object"""
        with pytest.raises(ValueError):
            Order.create(user_id=UUID("abdc284f-34a2-4bbe-966b-013b834cf889"), items=[], total_price=Money(-100.0))


class TestUser:
    def test_create_user_valid_email(self):
        """Проверка: создание пользователя с валидным email"""
        user = User.create(name="John Doe", email="test@example.com", password_hash="hashed_password")
        assert user.email.value == "test@example.com"

    def test_create_user_invalid_email(self):
        """Проверка: создание пользователя с невалидным email вызывает ошибку"""
        with pytest.raises(ValueError):
            User.create(name="John Doe", email="invalid-email", password_hash="hashed_password")
