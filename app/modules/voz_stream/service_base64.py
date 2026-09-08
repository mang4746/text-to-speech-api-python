import base64
# import tempfile
# import webbrowser
# from pathlib import Path

from fastapi import WebSocket

from app.core.logger import get_logger
from app.providers.tts.elevenlabs_provider import ElevenLabsTTSProvider
from app.providers.tts.schemas import TTSRequest
from app.providers.tts.exceptions import TTSProviderError
from app.shared.text_processors import TextPreprocessor
from .buffer_manager import TextStreamBuffer
from .schema import StreamOutputMessage

logger = get_logger(__name__)


class VozStreamBase64Service:
    """Servicio de voz en streaming para WebSocket."""

    def __init__(self, provider: ElevenLabsTTSProvider | None = None):
        self._provider = provider or ElevenLabsTTSProvider()
        self._buffer = TextStreamBuffer()

    async def handle_input(self, text: str, websocket: WebSocket) -> None:
        """Recibe texto incremental y genera audio cuando hay frases listas."""
        ready_phrases = self._buffer.append_text(text)

        for phrase in ready_phrases:
            await self._send_audio_chunk(phrase, websocket)

        await self._send_buffer_status(websocket)

    async def handle_flush(self, websocket: WebSocket) -> None:
        """Forzar el envío del texto pendiente en el buffer."""
        ready_phrases = self._buffer.flush()

        for phrase in ready_phrases:
            await self._send_audio_chunk(phrase, websocket)

        await self._send_buffer_status(websocket)

    async def close_session(self, websocket: WebSocket) -> None:
        """Cerrar sesión de streaming y procesar el buffer final."""
        if not self._buffer.is_empty():
            await self.handle_flush(websocket)

        await websocket.close()

    async def _send_audio_chunk(self, text: str, websocket: WebSocket) -> None:
        """Genera audio de texto y lo envía por WebSocket."""
        try:
            # Preprocesar texto antes de enviar a TTS
            pre = TextPreprocessor()
            clean_text = pre.preprocess(text)
            
            request = TTSRequest(text=clean_text)
            result = await self._provider.text_to_speech(request)

            # Codificar bytes a Base64 para enviar en JSON
            audio_base64 = base64.b64encode(result.audio_bytes).decode("utf-8")

            # [INI] Reproducción del audio generado (para pruebas)
            # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            #     temp_audio.write(result.audio_bytes)
            #     temp_audio_path = temp_audio.name
            # webbrowser.open(Path(temp_audio_path).as_uri())
            # [FIN] Reproducción del audio generado (para pruebas)

            payload = StreamOutputMessage(
                type="audio",
                text=text,
                audio_base64=audio_base64,
                mime_type=result.mime_type,
                voice_id=result.voice_id,
            ).model_dump(exclude_none=True)

            await websocket.send_json(payload)

            logger.debug("Audio chunk enviado: %s bytes para texto '%s'", len(result.audio_bytes), clean_text)

        except TTSProviderError as exc:
            logger.error("Error al generar audio por chunk: %s", exc.detail)
            await self._send_error(websocket, exc.detail)
        except Exception as exc:
            logger.exception("Error inesperado en el servicio de voz streaming")
            await self._send_error(websocket, str(exc))

    async def _send_buffer_status(self, websocket: WebSocket) -> None:
        payload = StreamOutputMessage(
            type="buffer",
            pending_text=self._buffer.pending_text,
        ).model_dump(exclude_none=True)

        await websocket.send_json(payload)

    async def _send_error(self, websocket: WebSocket, message: str) -> None:
        payload = StreamOutputMessage(type="error", message=message).model_dump(exclude_none=True)
        await websocket.send_json(payload)
