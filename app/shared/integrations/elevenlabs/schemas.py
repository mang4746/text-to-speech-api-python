from pydantic import BaseModel, Field


class ElevenLabsTTSRequest(BaseModel):
    """Petición enviada a ElevenLabs."""
    text: str = Field(..., description="Texto a convertir en audio")
    model_id: str = Field(..., description="Modelo de ElevenLabs")


class ElevenLabsTTSResponse(BaseModel):
    """Respuesta esperada de ElevenLabs cuando se usa JSON."""
    detail: str | None = Field(None, description="Detalle del mensaje de error")
    error: dict | None = Field(None, description="Error devuelto por ElevenLabs")
