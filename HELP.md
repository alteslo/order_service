## Docker
docker compose -f docker-compose.yml down -v
docker compose -f docker-compose.yml build --no-cache

docker compose -f docker-compose.yml down ; docker compose -f docker-compose.yml up --build

## Ruff
ruff check src/domain/
ruff format src/domain/

## Alembic
### Текущая ревизия в базе
docker compose exec api alembic current

### Все ревизии и их статус
docker compose exec api alembic history

### Список heads (обычно одна)
docker compose exec api alembic heads

### Если нужно откатить (осторожно!)
docker compose exec api alembic downgrade -1
### или до base (удалить все таблицы миграций)
docker compose exec api alembic downgrade base

### Автогенерация миграции
docker compose exec api alembic -c /app/alembic.ini revision --autogenerate -m "Initial migration"

###
docker compose exec api alembic -c alembic.ini upgrade head

## RabbitMQ:

### RabbitMQ Docs
<https://www.rabbitmq.com/tutorials>
<https://docs.aio-pika.com/>

### RabbitMQ service links
<http://127.0.0.1:15672/>

## Tests:
## Pytest local:
pytest src/tests/unit/domain/test_entities.py -v

## Pytest in Docker: