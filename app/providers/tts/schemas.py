from typing import Optional

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    """Modelo de entrada para un proveedor TTS."""
    text: str = Field(..., description="Texto a convertir en voz")
    voice_id: Optional[str] = Field(None, description="Identificador de voz a usar")
    model: Optional[str] = Field(None, description="Modelo de TTS a usar")


class TTSResponse(BaseModel):
    """Modelo de salida de un proveedor TTS."""
    audio_bytes: bytes = Field(..., description="Audio en bytes crudos")
    mime_type: str = Field(..., description="Tipo MIME del audio")
    voice_id: Optional[str] = Field(None, description="Identificador de voz usado")

    class Config:
        arbitrary_types_allowed = True
