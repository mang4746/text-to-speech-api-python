from typing import Optional

from app.core.config import settings
from app.core.logger import get_logger
from app.providers.tts.base import TTSProvider
from app.providers.tts.exceptions import TTSProviderError
from app.providers.tts.schemas import TTSRequest, TTSResponse
from app.shared.integrations.elevenlabs.client import ElevenLabsClient

logger = get_logger(__name__)


class ElevenLabsTTSProvider(TTSProvider):
    """Proveedor TTS que usa la API de ElevenLabs."""

    def __init__(self, client: Optional[ElevenLabsClient] = None):
        self._client = client or ElevenLabsClient(
            api_key=settings.ELEVENLABS_API_KEY,
            base_url=settings.ELEVENLABS_API_URL,
            voice_id=settings.ELEVENLABS_VOICE_ID,
            model=settings.ELEVENLABS_MODEL,
            timeout=settings.ELEVENLABS_TIMEOUT,
        )

    async def text_to_speech(self, request: TTSRequest) -> TTSResponse:
        if not request.text or not request.text.strip():
            raise TTSProviderError("El texto para generar voz no puede estar vacío.")

        try:
            audio_bytes, mime_type = await self._client.generate_tts(
                text=request.text,
                voice_id=request.voice_id or settings.ELEVENLABS_VOICE_ID,
                model=request.model or settings.ELEVENLABS_MODEL,
            )

            return TTSResponse(
                audio_bytes=audio_bytes,
                mime_type=mime_type,
                voice_id=request.voice_id or settings.ELEVENLABS_VOICE_ID,
            )
        except TTSProviderError:
            raise
        except Exception as exc:
            logger.exception("Error generando audio con ElevenLabs")
            raise TTSProviderError(str(exc)) from exc
