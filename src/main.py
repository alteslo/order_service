from fastapi import FastAPI

from src.core.config import settings
from src.core.logging import logger, setup_logging


setup_logging("DEBUG" if settings.debug else "INFO")

logger.info("Запуск сервиса {name}", name=settings.app_name)

app = FastAPI(
    title=settings.app_name,
    description="Order Management Service",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    logger.debug("Health check requested")
    return {"status": "ok"}
