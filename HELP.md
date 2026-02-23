## Docker
docker compose -f docker-compose.yml down -v
docker compose -f docker-compose.yml build --no-cache

docker compose -f docker-compose.yml down ; docker compose -f docker-compose.yml up --build

## Ruff
ruff check src/domain/
ruff format src/domain/

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