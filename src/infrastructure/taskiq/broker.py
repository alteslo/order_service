from taskiq import AsyncBroker
from taskiq_aio_pika import AioPikaBroker

from src.core.config import settings


broker: AsyncBroker = AioPikaBroker(settings.taskiq_broker_url)

def get_broker() -> AsyncBroker:
    return broker
