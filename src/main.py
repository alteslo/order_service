from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.logging import logger, setup_logging
from src.core.utils import setup_debugging
from src.infrastructure.cache import redis_client
from src.infrastructure.database import Base, engine, init_database
from src.infrastructure.message_broker import event_publisher


logger.info("Запуск сервиса {name}", name=settings.app_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация и закрытие подключений при старте/остановке"""
    # Настройка логирования и отладки
    setup_logging("DEBUG" if settings.debug else "INFO")
    setup_debugging("DEBUG" if settings.debug else "INFO")

    # Создание таблиц (для dev, в prod использовать alembic)
    await init_database(engine, Base, debug=settings.debug)
    await redis_client.connect()  # Подключение к Redis
    await event_publisher.connect()  # Подключение к RabbitMQ

    yield

    # Закрытие подключений
    await redis_client.close()
    await event_publisher.close()
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="Order Management Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Роутеры
# app.include_router(auth.router, prefix="/token", tags=["Auth"])
# app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/health")
async def health_check():
    logger.debug("Health check requested")
    return {"status": "ok"}
