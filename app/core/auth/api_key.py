from fastapi import Security
from fastapi.security import APIKeyHeader

from app.core.config import settings
from app.shared.exceptions import UnauthorizedError
from app.core.constants import ERROR_MESSAGES

api_key_header = APIKeyHeader(
    name="X-API-KEY",
    auto_error=False
)


async def validate_api_key(api_key: str = Security(api_key_header)):
    # Valida la API Key recibida en header `X-API-KEY`

    if not api_key:
        raise UnauthorizedError(ERROR_MESSAGES["missing_api_key"])

    if api_key != settings.API_KEY:
        raise UnauthorizedError(ERROR_MESSAGES["invalid_api_key"])

    return api_key
