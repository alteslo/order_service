from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings
from src.core.logging import logger


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""

    pass


engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор для получения сессии базы данных."""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_database(engine: AsyncEngine, base: type[DeclarativeBase], debug: bool = False) -> None:
    """
    Инициализация базы данных.

    В debug-режиме автоматически создаёт таблицы (для разработки).
    В production используется только Alembic миграции.
    """
    if debug:
        from src.infrastructure.database import models  # noqa: F401 - Импорт моделей для создания таблиц
        logger.debug("Debug mode: Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)
        logger.debug(f"Registered tables: {list(base.metadata.tables.keys())}")
        logger.debug("Database tables created successfully")
    else:
        logger.info("Production mode: Skipping table creation (use Alembic migrations)")
