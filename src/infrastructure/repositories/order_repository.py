from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Order
from src.domain.repositories import IOrderRepository
from src.domain.value_objects import Money
from src.infrastructure.database.models import OrderDB


class OrderRepository(IOrderRepository):
    """Реализация репозитория пользователей"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, order: Order) -> Order:
        db_order = OrderDB(
            user_id=order.user_id,
            items=order.items,
            total_price=order.total_price,
            status=order.status,
            created_at=order.created_at,
        )
        self._session.add(db_order)
        await self._session.flush()  # Получаем ID после вставки
        order.id = db_order.id
        return order

    async def get_by_id(self, order_id: UUID) -> Order | None:
        select_stmt = select(OrderDB).where(OrderDB.id == order_id)
        result = await self._session.execute(select_stmt)
        db_order = result.scalar_one_or_none()

        if db_order is None:
            return None
        return self._to_domain(db_order)

    async def update(self, order: Order) -> Order:
        select_stmt = select(OrderDB).where(OrderDB.id == order.id)
        result = await self._session.execute(select_stmt)
        db_order = result.scalar_one_or_none()

        if not db_order:
            raise ValueError(f"Order with id {order.id} not found")

        db_order.items = order.items
        db_order.total_price = order.total_price.amount
        db_order.status = order.status
        await self._session.flush()

        return self._to_domain(db_order)

    async def get_by_user_id(self, user_id: UUID) -> list[Order]:
        select_stmt = select(OrderDB).where(OrderDB.user_id == user_id)
        result = await self._session.execute(select_stmt)
        db_orders = result.scalars().all()

        return [self._to_domain(db_order) for db_order in db_orders]

    @staticmethod
    def _to_domain(db_order: OrderDB) -> Order:
        """Конвертация ORM модели в доменную сущность"""
        return Order(
            id=db_order.id,
            user_id=db_order.user_id,
            items=db_order.items,
            total_price=Money(db_order.total_price),
            status=db_order.status,
            created_at=db_order.created_at,
        )
