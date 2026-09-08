# TEXT-TO-SPEECH-API-PYTHON

**Motor de Voz en Streaming**  
**Versión:** 1.0.0 | **Fecha:** Septiembre 2026

---

## 1. Descripción General

Motor de generación de voz basado en texto diseñado para exponer un servicio REST y dos interfaces WebSocket de streaming. El núcleo está orientado a convertir texto en audio usando ElevenLabs como proveedor TTS.

### Alcance

- Conversión de texto a voz en un único request HTTP.
- Transmisión incremental de texto vía WebSocket con procesamiento de frases.
- Soporte de audio como Base64 y como frames binarios.
- Preprocesamiento de texto para mejorar la legibilidad del TTS.

### Casos de uso principales

- Generar audio de mensajes de texto en aplicaciones cliente.
- Procesar texto en tiempo real mediante WebSocket para reproducción progresiva.
- Enviar fragmentos de texto y recibir audio conforme se completa una frase.

### Flujo general de funcionamiento

1. La aplicación inicia con FastAPI y expone rutas bajo `/api`.
2. El cliente puede usar REST en `/api/voz/generate` o WebSocket en `/api/voz-stream/generate-base64` y `/api/voz-stream/generate`.
3. El servidor preprocesa el texto para normalizar URLs, números y caracteres especiales.
4. Se invoca ElevenLabs vía HTTP para obtener bytes de audio.
5. El audio se entrega como JSON Base64 o como metadata seguida de bytes binarios.



## 2. Arquitectura de la Solución

### Arquitectura general

La solución utiliza una capa de presentación FastAPI con routers modulares, servicios de dominio y una integración externa para TTS.

### Componentes principales

- `main.py`: Inicializa FastAPI, configura CORS, excepción y rutas.
- `run.py`: Ejecuta la aplicación con Uvicorn.
- `app/api/v1/routers.py`: Agrupa routers de módulos.
- `app/modules/voz/router.py`: Define el endpoint REST de voz.
- `app/modules/voz_stream/router.py`: Define endpoints de streaming WebSocket.
- `app/modules/voz/service.py`: Genera voz vía ElevenLabs y codifica Base64.
- `app/modules/voz_stream/service_base64.py`: Maneja WebSocket de audio Base64.
- `app/modules/voz_stream/service_binary.py`: Maneja WebSocket de audio binario.
- `app/shared/text_processors/preprocessor.py`: Normaliza texto antes de TTS.
- `app/providers/tts/elevenlabs_provider.py`: Cliente del proveedor ElevenLabs.
- `app/shared/integrations/elevenlabs/client.py`: Cliente HTTP con reintentos.

### Integraciones externas

- ElevenLabs TTS API para la generación de audio.
- `httpx` para llamadas HTTP asincrónicas.
- `tenacity` para reintentos con backoff.

### Flujo de procesamiento

1. Recepción de texto desde REST o WebSocket.
2. Preprocesamiento con `TextPreprocessor`.
3. Envío del texto al `ElevenLabsClient`.
4. Recepción de audio raw y empaquetado en respuesta.
5. En WebSocket, se envía estado de buffer y audio por fragmentos.

## 3. Tecnologías Utilizadas

### Frameworks y librerías

- Python
- FastAPI
- Uvicorn
- Pydantic
- httpx
- tenacity
- python-dotenv
- websockets

### Servicios externos

- ElevenLabs API

### Herramientas de desarrollo

- `uvicorn` para servidor ASGI
- `python-dotenv` para cargar `.env`
- `FastAPI` para documentación automática Swagger

### Dependencias relevantes

- `fastapi==0.108.0`
- `uvicorn==0.25.0`
- `pydantic==2.5.3`
- `httpx==0.26.0`
- `tenacity==9.1.4`
- `python-dotenv==1.0.0`

## 4. Estructura del Proyecto

### Organización de carpetas

- `app/`
  - `api/`: Router principal para versión 1.
  - `core/`: Configuración, logger y manejo de excepciones.
  - `db/`: Código comentado de Neo4j y Oracle (no activo).
  - `modules/`
    - `voz/`: Endpoint REST de generación de voz.
    - `voz_stream/`: WebSocket de streaming y buffer.
    - `health/`: Endpoint de estado.
  - `providers/tts/`: Proveedor TTS y modelos de solicitud/respuesta.
  - `shared/`: Utilidades comunes, integraciones y fábrica de respuestas.

### Componentes principales

- `app/core/config.py`: Variables de configuración centralizadas.
- `app/core/logger.py`: Logger con manejo de archivos rotativos.
- `app/core/exception_handlers.py`: Manejadores globales de errores.
- `app/shared/text_processors/preprocessor.py`: Normalización de texto para TTS.
- `app/modules/voz_stream/buffer_manager.py`: Buffer de frases para streaming.

### Convenciones de desarrollo

- Respuestas REST normalizadas con `ResponseFactory`.
- Tipado y validación con Pydantic.
- Modularidad clara entre routers, servicios e integraciones.
- Código comentado para componentes no activos en la versión actual.

## 5. Configuración del Sistema

### Variables de entorno

- `APP_NAME`
- `APP_DESCRIPTION`
- `APP_DOCS_URL`
- `APP_REDOC_URL`
- `APP_PORT`
- `APP_ENV`
- `CORS_ORIGINS`
- `CORS_METHODS`
- `CORS_HEADERS`
- `CORS_ALLOW_CREDENTIALS`
- `LOG_FILE_PATH`
- `LOG_LEVEL`
- `LOG_MAX_BYTES`
- `LOG_BACKUP_COUNT`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_API_URL`
- `ELEVENLABS_VOICE_ID`
- `ELEVENLABS_MODEL`
- `ELEVENLABS_TIMEOUT`

### Configuración de ElevenLabs

- `ELEVENLABS_API_KEY`: clave para autenticar las llamadas.
- `ELEVENLABS_API_URL`: URL base del servicio ElevenLabs.
- `ELEVENLABS_VOICE_ID`: voz configurada por defecto.
- `ELEVENLABS_MODEL`: modelo de voz (por defecto `eleven_multilingual_v2`).
- `ELEVENLABS_TIMEOUT`: timeout de llamadas HTTP.

### Parámetros generales

- `APP_PORT`: puerto en el que Uvicorn levanta la aplicación.
- `LOG_LEVEL`: nivel mínimo de logs.
- `CORS_*`: configuración de orígenes y cabeceras permitidas.

## 6. Procesamiento y Normalización de Texto

### Limpieza de texto

- Desescapa entidades HTML.
- Elimina emojis.
- Quita encabezados Markdown y símbolos `#`.
- Remueve formato Markdown simple (`**bold**`, `*italics*`, `` `code` ``, `[texto](url)`).

### Conversión de números

- Convierte números a texto con `NumberConverter`.
- Aplica conversión después de normalizar URLs y otros símbolos.

### Tratamiento de URLs

- Normaliza URLs a una forma legible para audio.
- Convierte `https://ejemplo.com/docs` a `ejemplo punto com barra docs`.
- Filtra segmentos sospechosos (hashes, tokens, caracteres especiales).

### Manejo de caracteres especiales

- Elimina caracteres de control no imprimibles.
- Reemplaza `°C` por `grados`.
- Convierte `N°` a `número`.
- Separa camelCase para mejorar la lectura.

### Reglas de pronunciación

- Se preserva la estructura de oraciones mediante puntos y signos de interrogación/exclamación.
- Se normalizan saltos de línea múltiples en uno solo.

## 7. Gestión de Voces

### Voz configurada

- Voz por defecto tomada de `ELEVENLABS_VOICE_ID`.
- Si el request no especifica voz, se utiliza esta voz configurada.

### Parámetros de generación

- `voice_id`: opcional en `TTSRequest`.
- `model`: opcional en `TTSRequest`.
- `mime_type`: devuelto desde ElevenLabs.

### Criterios de selección

- Se prioriza el `voice_id` enviado en la petición.
- En ausencia de `voice_id`, se usa el valor de `ELEVENLABS_VOICE_ID`.

## 7. Generación de Audio

### Flujo de generación

1. Texto limpio es generado por `TextPreprocessor`.
2. Se crea un `TTSRequest`.
3. `ElevenLabsTTSProvider` invoca `ElevenLabsClient.generate_tts()`.
4. Se recibe `audio_bytes` y `mime_type`.
5. Se empaqueta la respuesta o se convierte a Base64 según el canal.

### Streaming de audio

- `/api/voz-stream/generate-base64`: envía objetos JSON con audio codificado en Base64.
- `/api/voz-stream/generate`: envía metadata JSON `audio_frame` y luego bytes de audio binarios.
- El buffer segmenta el texto cuando detecta frases terminadas o cuando se fuerza `flush`.

### Manejo de errores

- Errores de validación de WebSocket retornan `type: error`.
- Fallos en ElevenLabs devuelven mensajes de error JSON.
- Excepciones HTTP globales se manejan con `ResponseFactory.error`.

### Consideraciones de rendimiento

- `TextStreamBuffer` segmenta frases y evita enviar texto parcial sin puntuación.
- `ElevenLabsClient` usa reintentos con backoff exponencial para mejorar resiliencia.
- `logger` usa rotación de archivos para evitar archivos grandes.

## 8. API y Servicios Disponibles

### Endpoints REST

- `GET /api/health`
  - Retorna estado `UP`, versión y datos básicos de la aplicación.
- `POST /api/voz/generate`
  - Genera audio desde texto y devuelve Base64 en JSON.

### Comunicación WebSocket

- `ws://<host>/api/voz-stream/generate-base64`
  - Recibe mensajes JSON y responde audio Base64.
- `ws://<host>/api/voz-stream/generate`
  - Recibe mensajes JSON y responde metadata + bytes de audio.
- `GET /api/voz-stream/info`
  - Documenta el uso de los WebSockets para Swagger.

### Formato de mensajes

#### Mensajes de cliente WebSocket

- `input`: `{ "type": "input", "text": "Hola, esto es un ejemplo" }`
- `flush`: `{ "type": "flush" }`
- `close`: `{ "type": "close" }`

#### Respuestas WebSocket Base64

- `audio`: audio codificado en Base64.
- `buffer`: estado del texto pendiente.
- `error`: mensaje de error.

#### Respuestas WebSocket binario

- `audio_frame`: metadata antes de enviar bytes binarios.
- `buffer_status`: estado del texto pendiente.
- `error`: mensaje de error.

### Ejemplos de uso

#### REST

POST `/api/voz/generate`

```json
{ "text": "Hola, ¿cómo estás?" }
```

Respuesta esperada: JSON con `audio_base64`, `mime_type` y `voice_id`.

#### WebSocket Base64

Enviar:

```json
{ "type": "input", "text": "Este es un ejemplo." }
```

Responderá con un mensaje `audio` y luego `buffer`.

### Seguridad

#### Gestión de credenciales

- La clave de ElevenLabs se configura en `ELEVENLABS_API_KEY`.
- No hay encriptación específica implementada en el código.

#### Protección de servicios

- No hay autenticación activa en los endpoints REST o WebSocket.
- Algunos componentes de auth y DB están presentes pero comentados.

#### Buenas prácticas

- Mantener la clave `ELEVENLABS_API_KEY` fuera del repositorio.
- Usar CORS restringido en producción vía `CORS_ORIGINS`.

## 9. Monitoreo y Registro

### Logs

- Se genera un archivo de log en `logs/app.log`.
- El logger rota archivos según `LOG_MAX_BYTES` y `LOG_BACKUP_COUNT`.

### Seguimiento de errores

- Errores se registran con el logger de la aplicación.
- Excepciones de ElevenLabs y WebSocket quedan en logs.


## 10. Instalación

### Con Docker (Recomendado)

```bash
# Clonar repositorio
git clone <repo-url>
cd WS-PYTHON-TEXT-TO-SPEECH

# Crear archivo .env con credenciales
cp .env.example .env

# Editar el archivo .env y configurar credenciales,
nano .env

# Ejecutar script de inicialización (si aplica)
# Puede construir imágenes, validar dependencias
# o preparar el entorno de ejecución
./docker-start.sh

# Levantar todos los servicios definidos en docker-compose.yml
docker compose up -d

# Verificar el estado de los contenedores
docker compose ps

# Visualizar logs en tiempo real
docker compose logs -f

# Detener los servicios
docker compose down
```

La API estará disponible en `http://localhost:<APP_PORT>`.

### Instalación Local

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno
# Windows:
.venv\Scripts\activate
# Unix/macOS:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecución
python run.py
```

API disponible en `http://localhost:<APP_PORT>`.

---

## 11. Consideraciones Operativas

### Recomendaciones

- Activar CORS restrictivo en producción.
- Proteger la clave de ElevenLabs y rotar la credencial.
- Agregar un mecanismo de autenticación si el servicio se publica.

### Mantenimiento

- Mantener actualizadas las dependencias en `requirements.txt`.
- Revisar logs periódicamente para errores de integración.

### Buenas prácticas de operación

- Ejecutar la aplicación con un gestor de procesos o contenedor.
- Asegurar la variable `ELEVENLABS_API_KEY` en el entorno.

## 12. Anexos

### Ejemplos

- WebSocket `input`: `{ "type": "input", "text": "Hola mundo." }`
- WebSocket `flush`: `{ "type": "flush" }`
- WebSocket `close`: `{ "type": "close" }`

### Configuraciones de referencia

- `APP_PORT=8000`
- `ELEVENLABS_API_URL=https://api.elevenlabs.io/v1`
- `ELEVENLABS_MODEL=eleven_multilingual_v2`

### Enlaces de interés

- Swagger UI: `/docs`
- ReDoc: `/redoc`
