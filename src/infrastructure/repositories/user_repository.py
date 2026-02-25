from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import User
from src.domain.repositories import IUserRepository
from src.domain.value_objects import Email
from src.infrastructure.database.models import UserDB


class UserRepository(IUserRepository):
    """Реализация репозитория пользователей"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, user: User) -> User:
        db_user = UserDB(
            name=user.name,
            email=user.email.value,
            password_hash=user.password_hash,
            created_at=user.created_at,
        )
        self._session.add(db_user)
        await self._session.flush()  # Получаем ID после вставки
        user.id = db_user.id
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        select_stmt = select(UserDB).where(UserDB.id == user_id)
        result = await self._session.execute(select_stmt)
        db_user = result.scalar_one_or_none()

        if db_user is None:
            return None
        return self._to_domain(db_user)

    async def get_by_email(self, email: str) -> User | None:
        select_stmt = select(UserDB).where(UserDB.email == email)
        result = await self._session.execute(select_stmt)
        db_user = result.scalar_one_or_none()

        if db_user is None:
            return None
        return self._to_domain(db_user)

    @staticmethod
    def _to_domain(db_user: UserDB) -> User:
        """Конвертация ORM модели в доменную сущность"""
        return User(
            id=db_user.id,
            name=db_user.name,
            email=Email(db_user.email),
            password_hash=db_user.password_hash,
            created_at=db_user.created_at,
        )
