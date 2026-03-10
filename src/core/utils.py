import debugpy

from src.core.logging import logger


def setup_debugging(level: str = "INFO") -> None:
    if level == "DEBUG":
        debugpy.listen(("0.0.0.0", 5678))
        logger.debug("Debugging enabled on port 5678")
    else:
        logger.info("Debugging not enabled (set LOG_LEVEL=DEBUG to enable)")
