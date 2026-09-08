import logging
from logging.handlers import RotatingFileHandler

from app.core.config import settings


def setup_logger() -> logging.Logger:
    # Configura el logger raíz una sola vez.
    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.debug("Logger ya configurado. Omitiendo configuración duplicada.")
        return root_logger

    settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
    settings.LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        settings.LOG_FILE_PATH,
        maxBytes=settings.MAX_LOG_FILE_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    file_handler.setFormatter(formatter)

    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Integrar logs de uvicorn
    for logger_name in ("uvicorn.access", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = root_logger.handlers
        uvicorn_logger.setLevel(logging.INFO)
        uvicorn_logger.propagate = False  # evita duplicados

    # Silenciar ruido externo
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("neo4j").setLevel(logging.WARNING)

    root_logger.info("Logger configurado: %s", settings.LOG_FILE_PATH)
    return root_logger


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
