import asyncio

from src.core.logging import logger
from src.infrastructure.taskiq.broker import broker


@broker.task
async def process_order_task(order_id: str) -> None:
    """
    Фоновая задача обработки заказа.
    Согласно ТЗ: sleep(2) + print
    """
    logger.info(f"Starting processing order {order_id}")
    await asyncio.sleep(2)  # Имитация сложной обработки
    logger.info(f"Order {order_id} processed")
