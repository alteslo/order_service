import logging
import sys

from loguru import logger


def setup_logging(level: str = "INFO") -> None:
    logger.remove()  # Удаляем стандартный обработчик loguru

    dev_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    prod_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} | {message}"

    # Добавляем свой обработчик в stdout с форматированием
    if level == "DEBUG":
        logger.add(sys.stdout, level=level, format=dev_format, colorize=True)
        logger.info("Режим разработки: логирование настроено для вывода в консоль.")
    else:
        logger.add(
            sys.stdout,
            level=level,
            format=prod_format,
            colorize=True,
        )
        logger.info("Режим продакшена: логирование настроено для вывода в консоль и файл.")

    # Перехватываем стандартные логи (uvicorn, sqlalchemy и т.д.)
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Устанавливаем уровень для логгеров библиотек
    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)
    logging.getLogger("sqlalchemy").setLevel(level)


logger = logger
