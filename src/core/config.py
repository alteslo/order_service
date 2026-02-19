from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = "OrderService"
    debug: bool = False

    # Database
    database_url: str

    # Redis
    redis_url: str

    # RabbitMQ
    rabbitmq_url: str

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Taskiq
    taskiq_broker_url: str

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