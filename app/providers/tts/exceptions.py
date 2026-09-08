from app.shared.exceptions import AppException


class TTSProviderError(AppException):
    """Excepción base para errores de proveedores TTS."""

    def __init__(self, message: str = "Error en el servicio TTS"):
        super().__init__(status_code=502, detail=message)
