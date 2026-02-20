from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # Application
    app_name: str = "OrderService"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/orders_db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    # Security
    secret_key: str = "12345"  #! Изменить в продакшене
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Taskiq
    taskiq_broker_url: str = "amqp://guest:guest@localhost:5672/"

    @property
    def redis_dsn(self) -> str:
        return self.redis_url

    @property
    def rabbitmq_dsn(self) -> str:
        return self.rabbitmq_url


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
