import base64

from app.core.logger import get_logger
from app.providers.tts.elevenlabs_provider import ElevenLabsTTSProvider
from app.providers.tts.schemas import TTSRequest
from app.providers.tts.exceptions import TTSProviderError
from app.shared.text_processors import TextPreprocessor

logger = get_logger(__name__)

provider = ElevenLabsTTSProvider()


async def generate_voz(text: str):
    try:

        # Preprocesar texto antes de enviar a TTS
        pre = TextPreprocessor()
        clean_text = pre.preprocess(text)

        request = TTSRequest(text=clean_text)

        result = await provider.text_to_speech(request)

        # Codificar bytes a Base64 para la respuesta JSON
        audio_base64 = base64.b64encode(result.audio_bytes).decode("utf-8")

        # [INI] Reproducción del audio generado (para pruebas)
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        #     temp_audio.write(result.audio_bytes)
        #     temp_audio_path = temp_audio.name
        # webbrowser.open(Path(temp_audio_path).as_uri())
        # [FIN] Reproducción del audio generado (para pruebas)

        return {
            "texto": text,
            "audio_base64": audio_base64,
            "mime_type": result.mime_type,
            "voice_id": result.voice_id,
        }

    except TTSProviderError as exc:
        logger.error(f"Error en el proveedor de voz: {exc.detail}")
        raise
    except Exception as e:
        logger.exception(f"Error al generar voz: {str(e)}")
        raise
