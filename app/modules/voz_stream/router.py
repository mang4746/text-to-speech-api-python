import json
from typing import Any, Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.logger import get_logger
from .schema import (
    StreamInputMessage,
    WebSocketCommand,
    WebSocketEndpointInfo,
    WebSocketInfo,
    WebSocketOutputExample,
)
from .service_base64 import VozStreamBase64Service
from .service_binary import VozStreamBinaryService

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/info",
    summary="Información del WebSocket de streaming de voz",
    description=(
        "Devuelve documentación sobre cómo establecer la conexión WebSocket, "
        "qué mensajes puede enviar el cliente y qué mensajes puede recibir del servidor."
    ),
    response_model=WebSocketInfo,
)
async def websocket_stream_info():
    return WebSocketInfo(
        description="Documentación de los endpoints WebSocket de streaming de voz en el servicio.",
        websocket_url_template="ws://<host>/api/voz-stream/<endpoint>",
        endpoints=[
            WebSocketEndpointInfo(
                path="/api/voz-stream/generate-base64",
                description="Envía texto incremental y recibe audio codificado en Base64 en mensajes JSON.",
                example_connection="ws://<host>/api/voz-stream/generate-base64",
                binary=False,
            ),
            WebSocketEndpointInfo(
                path="/api/voz-stream/generate",
                description="Envía texto incremental y recibe audio mediante frames binarios con metadata JSON.",
                example_connection="ws://<host>/api/voz-stream/generate",
                binary=True,
            ),
        ],
        commands=[
            WebSocketCommand(
                type="input",
                description="Envía texto incremental para procesar y generar audio cuando hay frases completas.",
                payload_example={"type": "input", "text": "Hola, esto es un ejemplo."},
            ),
            WebSocketCommand(
                type="flush",
                description="Solicita el procesamiento inmediato del texto pendiente en el buffer.",
                payload_example={"type": "flush"},
            ),
            WebSocketCommand(
                type="close",
                description="Cierra la sesión de streaming y procesa cualquier texto pendiente.",
                payload_example={"type": "close"},
            ),
        ],
        responses=[
            WebSocketOutputExample(
                type="audio",
                description="Mensaje JSON que incluye audio codificado en Base64 para el endpoint /generate-base64.",
                example_payload={
                    "type": "audio",
                    "text": "Hola mundo",
                    "audio_base64": "<base64>...",
                    "mime_type": "audio/mpeg",
                    "voice_id": "default",
                },
            ),
            WebSocketOutputExample(
                type="buffer",
                description="Estado del buffer después de recibir texto o un flush.",
                example_payload={
                    "type": "buffer",
                    "pending_text": "Texto aún no procesado...",
                },
            ),
            WebSocketOutputExample(
                type="audio_frame",
                description="Metadata JSON enviada antes del frame binario de audio en /generate.",
                example_payload={
                    "type": "audio_frame",
                    "text": "Hola mundo",
                    "mime_type": "audio/mpeg",
                    "voice_id": "default",
                    "audio_length": 12345,
                },
            ),
            WebSocketOutputExample(
                type="buffer_status",
                description="Estado del buffer para el endpoint binario /generate.",
                example_payload={
                    "type": "buffer_status",
                    "pending_text": "Texto aún no procesado...",
                },
            ),
            WebSocketOutputExample(
                type="error",
                description="Mensaje de error que indica fallo de validación o interno.",
                example_payload={
                    "type": "error",
                    "message": "Mensaje JSON inválido.",
                },
            ),
        ],
        notes=(
            "Los endpoints WebSocket no aparecen directamente como operaciones en OpenAPI. "
            "Por eso este recurso HTTP ofrece documentación y ejemplos dentro de Swagger UI."
        ),
    )


@router.websocket("/generate-base64")
async def websocket_voz_stream(websocket: WebSocket):
    """WebSocket para procesar texto incremental y devolver audio en Base64."""
    await websocket.accept()
    service = VozStreamBase64Service()

    try:
        while True:
            raw_message = await websocket.receive_text()
            try:
                payload = json.loads(raw_message)
            except json.JSONDecodeError as exc:
                await websocket.send_json({"type": "error", "message": "Mensaje JSON inválido."})
                logger.warning("Mensaje WebSocket inválido: %s", exc)
                continue

            try:
                message = StreamInputMessage(**payload)
            except Exception as exc:
                await websocket.send_json({"type": "error", "message": str(exc)})
                logger.warning("Validación de mensaje WebSocket fallida: %s", exc)
                continue

            if message.type == "input":
                logger.debug("Texto recibido para procesamiento: '%s'", message.text)
                await service.handle_input(message.text or "", websocket)
            elif message.type == "flush":
                await service.handle_flush(websocket)
            elif message.type == "close":
                await service.close_session(websocket)
                break

    except WebSocketDisconnect:
        logger.info("Cliente WebSocket de voz streaming desconectado.")
    except Exception as e:
        logger.exception(f"Error en el WebSocket de voz streaming: {str(e)}")
        try:
            await websocket.send_json({"type": "error", "message": "Error interno del servidor en streaming."})
            await websocket.close(code=1011)
        except Exception:
            pass


@router.websocket("/generate")
async def websocket_voz_stream_binary(websocket: WebSocket):
    """WebSocket para procesar texto incremental y devolver audio mediante binary frames."""
    await websocket.accept()
    service = VozStreamBinaryService()

    try:
        while True:
            raw_message = await websocket.receive_text()
            try:
                payload = json.loads(raw_message)
            except json.JSONDecodeError as exc:
                await websocket.send_json({"type": "error", "message": "Mensaje JSON inválido."})
                logger.warning("Mensaje WebSocket binario inválido: %s", exc)
                continue

            try:
                message = StreamInputMessage(**payload)
            except Exception as exc:
                await websocket.send_json({"type": "error", "message": str(exc)})
                logger.warning("Validación de mensaje WebSocket binario fallida: %s", exc)
                continue

            if message.type == "input":
                logger.debug("Texto recibido para procesamiento: '%s'", message.text)
                await service.handle_input(message.text or "", websocket)
            elif message.type == "flush":
                await service.handle_flush(websocket)
            elif message.type == "close":
                await service.close_session(websocket)
                break

    except WebSocketDisconnect:
        logger.info("Cliente WebSocket de voz streaming binario desconectado.")
    except Exception as e:
        logger.exception(f"Error en el WebSocket de voz streaming binario: {str(e)}")
        try:
            await websocket.send_json({"type": "error", "message": "Error interno del servidor en streaming binario."})
            await websocket.close(code=1011)
        except Exception:
            pass
