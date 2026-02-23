from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import Order, User


class IUserRepository(ABC):
    """Интерфейс репозитория для работы с пользователями"""

    @abstractmethod
    async def add(self, user: User) -> User:
        """Сохранить нового пользователя в репозитории"""
        ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Получить пользователя по ID"""
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Получить пользователя по email"""
        ...


class IOrderRepository(ABC):
    """Интерфейс репозитория для работы с заказами"""

    @abstractmethod
    async def add(self, order) -> None:
        """Сохранить новый заказ"""
        ...

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None:
        """Получить заказ по ID"""
        ...

    @abstractmethod
    async def update(self, order: Order) -> Order:
        """Обновить существующий заказ"""
        ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Order]:
        """Получить все заказы пользователя"""
        ...


class IUnitOfWork(ABC):
    """
    Unit of Work - паттерн для управления транзакциями.
    Гарантирует атомарность операций.
    """

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self) -> None:
        """Зафиксировать транзакцию"""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Откатить транзакцию"""
        ...

    @property
    @abstractmethod
    def orders(self) -> IOrderRepository:
        pass

    @property
    @abstractmethod
    def users(self) -> IUserRepository:
        pass
