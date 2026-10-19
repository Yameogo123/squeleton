"""Loguru setup: one sink, request id on every line, JSON in prod, std logging (uvicorn) routed through it."""

import logging
import sys

from loguru import logger

from {{ cookiecutter.package_slug }}.core.config import settings

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
    "<magenta>{extra[request_id]}</magenta> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    logger.remove()
    logger.configure(extra={"request_id": "-"})
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=LOG_FORMAT,
        serialize=settings.is_prod,  # JSON lines in prod (log collectors)
        backtrace=not settings.is_prod,
        diagnose=not settings.is_prod,  # diagnose prints variable values: never in prod
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    for name in ("uvicorn", "uvicorn.error", "fastapi"):
        logging.getLogger(name).handlers = [InterceptHandler()]
        logging.getLogger(name).propagate = False
    # access lines are produced by RequestContextMiddleware (with request id + duration)
    logging.getLogger("uvicorn.access").disabled = True
