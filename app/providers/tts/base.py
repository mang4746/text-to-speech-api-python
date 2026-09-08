from abc import ABC, abstractmethod

from app.providers.tts.schemas import TTSRequest, TTSResponse


class TTSProvider(ABC):
    """Interfaz abstracta para proveedores de Text-to-Speech."""

    @abstractmethod
    async def text_to_speech(self, request: TTSRequest) -> TTSResponse:
        """Convierte texto en audio TTS."""
        raise NotImplementedError
