# ==========================================
# Stage 1: Builder
# ==========================================
FROM python:3.11-slim as builder

# Устанавливаем uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Копируем файлы зависимостей первыми для кеширования слоев
COPY pyproject.toml .
COPY README.md .

# Создаем виртуальное окружение и устанавливаем зависимости
# --frozen: использует точные версии из uv.lock (если есть)
# --no-dev: не устанавливает зависимости для разработки в продакшен
RUN uv venv /app/.venv && \
    UV_PROJECT_ENVIRONMENT=/app/.venv uv sync --frozen --no-dev

# Копируем исходный код
COPY src/ ./src/
COPY alembic.ini .
COPY migrations/ ./migrations/

# Компилируем байт-код для ускорения запуска
RUN python -m compileall src/

# ==========================================
# Stage 2: Runtime
# ==========================================
FROM python:3.14.3-slim as runtime

# Создаем пользователя для безопасности (не root)
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Копируем виртуальное окружение из builder
COPY --from=builder /app/.venv /app/.venv

# Копируем исходный код
COPY --from=builder /app/src ./src
COPY --from=builder /app/alembic.ini .
COPY --from=builder /app/migrations ./migrations

# Добавляем venv в PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Переключаемся на пользователя appuser
USER appuser

# Команда по умолчанию (переопределяется в docker-compose)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]