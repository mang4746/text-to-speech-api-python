import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core.logger import get_logger
from app.core.config import settings
from app.shared.integrations.elevenlabs.exceptions import ElevenLabsIntegrationError

logger = get_logger(__name__)


class ElevenLabsClient:
    """Cliente HTTP para la API de ElevenLabs."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        voice_id: str,
        model: str,
        timeout: int = 30,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.voice_id = voice_id
        self.model = model
        self.timeout = timeout

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def generate_tts(self, text: str, voice_id: str = None, model: str = None) -> tuple[bytes, str]:
        if not self.api_key:
            raise ElevenLabsIntegrationError("Falta la clave ELEVENLABS_API_KEY.")

        voice_id = voice_id or self.voice_id
        if not voice_id:
            raise ElevenLabsIntegrationError("Falta el identificador de voz ELEVENLABS_VOICE_ID.")

        model = model or self.model
        if not model:
            raise ElevenLabsIntegrationError("Falta el modelo de ElevenLabs ELEVENLABS_MODEL.")

        url = f"{self.base_url}/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": model,
        }

        logger.debug("Enviando request a ElevenLabs", extra={"url": url})

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload, headers=headers)
        except httpx.HTTPError as exc:
            logger.exception("Error de red al llamar a ElevenLabs")
            raise ElevenLabsIntegrationError(str(exc)) from exc

        if response.status_code >= 400:
            message = response.text
            try:
                body = response.json()
                message = body.get("error", {}).get("message", message)
            except Exception:
                pass
            raise ElevenLabsIntegrationError(
                f"ElevenLabs API error {response.status_code}: {message}"
            )

        return response.content, response.headers.get("Content-Type", "audio/mpeg")
