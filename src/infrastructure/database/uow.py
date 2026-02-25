


from src.domain.repositories import IOrderRepository, IUnitOfWork, IUserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.order_repository import OrderRepository


class UnitOfWork(IUnitOfWork):
    """Реализация паттерна Unit of Work для управления транзакциями базы данных."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._user_repo: UserRepository | None = None
        self._order_repo: OrderRepository | None = None

    async def __aenter__(self):
        """Начало блока with - открытие транзакции."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Конец блока with - коммит или откат транзакции."""
        if exc_type:
            await self._session.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def close(self) -> None:
        await self._session.close()

    @property
    def users(self) -> IUserRepository:
        if self._user_repo is None:
            self._user_repo = UserRepository(self._session)
        return self._user_repo

    @property
    def orders(self) -> IOrderRepository:
        if self._order_repo is None:
            self._order_repo = OrderRepository(self._session)
        return self._order_repo
