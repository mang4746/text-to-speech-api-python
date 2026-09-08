import json
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, root_validator


class StreamInputMessage(BaseModel):
    type: Literal["input", "flush", "close"] = Field(
        ..., description="Tipo de mensaje websocket enviado por el frontend"
    )
    text: Optional[str] = Field(None, description="Texto incremental a procesar")

    @root_validator(skip_on_failure=True)
    def validate_input_text(cls, values):
        message_type = values.get("type")
        text = values.get("text")

        # Para streaming letra por letra permitimos que `text` contenga solo espacios;
        # solo exigimos que el campo exista (no sea None) cuando type == 'input'.
        if message_type == "input" and text is None:
            raise ValueError("El campo 'text' es obligatorio cuando type='input'.")

        return values

    @classmethod
    def parse_text(cls, raw_message: str) -> "StreamInputMessage":
        return cls.parse_raw(raw_message)


class StreamOutputMessage(BaseModel):
    type: Literal["audio", "buffer", "status", "error"]
    text: Optional[str] = None
    audio_base64: Optional[str] = None
    mime_type: Optional[str] = None
    voice_id: Optional[str] = None
    pending_text: Optional[str] = None
    message: Optional[str] = None


# Modelos para documentación de WebSocket


class WebSocketEndpointInfo(BaseModel):
    path: str = Field(..., description="Ruta del endpoint WebSocket relativa al prefijo /api/voz-stream")
    description: str = Field(..., description="Descripción de cómo funciona este endpoint WebSocket")
    example_connection: str = Field(..., description="Ejemplo de URL de conexión WebSocket")
    binary: bool = Field(False, description="Indica si el endpoint utiliza frames binarios")


class WebSocketCommand(BaseModel):
    type: Literal["input", "flush", "close"]
    description: str
    payload_example: Dict[str, Any]


class WebSocketOutputExample(BaseModel):
    type: str
    description: str
    example_payload: Dict[str, Any]


class WebSocketInfo(BaseModel):
    description: str = Field(..., description="Descripción del comportamiento general del WebSocket")
    websocket_url_template: str = Field(..., description="Plantilla de URL para conexiones WebSocket")
    endpoints: List[WebSocketEndpointInfo] = Field(..., description="Lista de endpoints de streaming disponibles")
    commands: List[WebSocketCommand] = Field(..., description="Mensajes que puede enviar el cliente")
    responses: List[WebSocketOutputExample] = Field(..., description="Tipos de mensajes que puede recibir el cliente")
    notes: Optional[str] = Field(None, description="Notas adicionales sobre la implementación")
