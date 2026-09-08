from pathlib import Path

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def print_banner():
    try:
        banner_path = Path(__file__).resolve().parents[2] / "banner.txt"

        with open(banner_path, "r", encoding="utf-8") as file:
            banner_template = file.read()

        banner = banner_template.format(
            APP_NAME=settings.APP_NAME,
            APP_VERSION=settings.APP_VERSION,
            APP_ENV=settings.APP_ENV,
            LOG_LEVEL=settings.LOG_LEVEL,
        )

        print("\n" + banner + "\n")

    except Exception as e:
        logger.warning(f"No se pudo cargar el banner: {e}")