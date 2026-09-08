from fastapi import WebSocket

from app.core.logger import get_logger
from app.providers.tts.elevenlabs_provider import ElevenLabsTTSProvider
from app.providers.tts.schemas import TTSRequest
from app.providers.tts.exceptions import TTSProviderError
from app.shared.text_processors import TextPreprocessor
from .buffer_manager import TextStreamBuffer

logger = get_logger(__name__)


class VozStreamBinaryService:
    """Servicio de voz en streaming con binary frames (sin Base64)."""

    def __init__(self, provider: ElevenLabsTTSProvider | None = None):
        self._provider = provider or ElevenLabsTTSProvider()
        self._buffer = TextStreamBuffer()

    async def handle_input(self, text: str, websocket: WebSocket) -> None:
        """Recibe texto incremental y genera audio cuando hay frases listas."""
        ready_phrases = self._buffer.append_text(text)

        for phrase in ready_phrases:
            await self._send_audio_chunk_binary(phrase, websocket)

        await self._send_buffer_status(websocket)

    async def handle_flush(self, websocket: WebSocket) -> None:
        """Forzar el envío del texto pendiente en el buffer."""
        ready_phrases = self._buffer.flush()

        for phrase in ready_phrases:
            await self._send_audio_chunk_binary(phrase, websocket)

        await self._send_buffer_status(websocket)

    async def close_session(self, websocket: WebSocket) -> None:
        """Cerrar sesión de streaming y procesar el buffer final."""
        if not self._buffer.is_empty():
            await self.handle_flush(websocket)

        await websocket.close()

    async def _send_audio_chunk_binary(self, text: str, websocket: WebSocket) -> None:
        """Genera audio de texto y lo envía como binary frame."""
        try:
            # Preprocesar texto antes de enviar a TTS
            pre = TextPreprocessor()
            clean_text = pre.preprocess(text)

            request = TTSRequest(text=clean_text)
            result = await self._provider.text_to_speech(request)

            # Enviar metadata en JSON
            metadata = {
                "type": "audio_frame",
                "text": text,
                "mime_type": result.mime_type,
                "voice_id": result.voice_id,
                "audio_length": len(result.audio_bytes),
            }
            await websocket.send_json(metadata)

            # Enviar audio como binary frame directamente (sin decodificar)
            await websocket.send_bytes(result.audio_bytes)

            logger.debug("Audio chunk enviado: %s bytes para texto '%s'", len(result.audio_bytes), clean_text)

        except TTSProviderError as exc:
            logger.error("Error al generar audio por chunk: %s", exc.detail)
            await self._send_error(websocket, exc.detail)
        except Exception as exc:
            logger.exception("Error inesperado en el servicio de voz streaming binario")
            await self._send_error(websocket, str(exc))

    async def _send_buffer_status(self, websocket: WebSocket) -> None:
        """Envía el estado actual del buffer."""
        payload = {
            "type": "buffer_status",
            "pending_text": self._buffer.pending_text,
        }
        await websocket.send_json(payload)

    async def _send_error(self, websocket: WebSocket, message: str) -> None:
        """Envía un mensaje de error."""
        payload = {
            "type": "error",
            "message": message,
        }
        await websocket.send_json(payload)
