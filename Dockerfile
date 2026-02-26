# ==========================================
# Stage 1: Builder
# ==========================================
FROM python:3.14.3-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Устанавливаем только зависимости (без самого проекта)
RUN uv sync --no-dev --locked --no-editable --no-install-project

# Копируем код проекта и финализируем venv
COPY migrations/ ./migrations
COPY src/ ./src
COPY alembic.ini src/ ./

RUN uv sync --no-dev --locked --no-editable

# ==========================================
# Stage 2: Runtime
# ==========================================
FROM python:3.14.3-slim AS runtime

# Создаём группу и пользователя (без домашней директории, без shell)
RUN groupadd -r appgroup --gid 1000 && \
    useradd -r -g appgroup --uid 1000 -s /sbin/nologin -m appuser

# Переключаемся на не-root пользователя как можно раньше
USER appuser

WORKDIR /app

# Копируем виртуальное окружение
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

# Копируем нужные файлы для alembic (если миграции запускаются в проде)
COPY --from=builder --chown=appuser:appgroup /app/src ./src
COPY --from=builder --chown=appuser:appgroup /app/alembic.ini .
COPY --from=builder --chown=appuser:appgroup /app/migrations ./migrations

ENV PATH="/app/.venv/bin:$PATH"

# Команда по умолчанию (в dev переопределяется в docker-compose)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]