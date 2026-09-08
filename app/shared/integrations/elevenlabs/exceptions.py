from app.shared.exceptions import AppException


class ElevenLabsIntegrationError(AppException):
    """Error de integración con ElevenLabs."""

    def __init__(self, message: str = "Error de integración con ElevenLabs"):
        super().__init__(status_code=502, detail=message)
