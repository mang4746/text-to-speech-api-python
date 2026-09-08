import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))

_version_file = Path(__file__).parent.parent.parent / 'VERSION'
_app_version = _version_file.read_text().strip() if _version_file.exists() else "1.0.0"

class Settings:
    """Configuración centralizada de la aplicación."""

    # App settings
    APP_NAME: str = os.environ.get('APP_NAME', "Gemelo Digital Cliente 360")
    APP_DESCRIPTION: str = os.environ.get('APP_DESCRIPTION', "API Gemelo Digital de Cliente BDP")
    APP_VERSION: str = _app_version
    APP_DOCS_URL: str = os.environ.get('APP_DOCS_URL', "/docs")
    APP_REDOC_URL: str = os.environ.get('APP_REDOC_URL', "/redoc")
    APP_PORT: int = int(os.environ.get('APP_PORT', '8000'))
    APP_ENV: str = os.environ.get('APP_ENV', 'development')
    APP_RELOAD=bool(os.environ.get('APP_RELOAD', 'false').lower() in ('true', '1', 'yes'))

    # Api Key
    API_KEY: str = os.environ.get('API_KEY', 'xxx-xxx-xxx-xxx-xxx')

    # CORS settings
    CORS_ORIGINS: List[str] = [ origin.strip() for origin in os.environ.get("CORS_ORIGINS", "*").split(",") if origin.strip() ]
    CORS_METHODS: List[str] = [ method.strip().upper() for method in os.environ.get("CORS_METHODS", "*").split(",") if method.strip() ]
    CORS_HEADERS: List[str] = [ header.strip() for header in os.environ.get("CORS_HEADERS", "*").split(",") if header.strip() ]
    CORS_ALLOW_CREDENTIALS: bool = os.environ.get("CORS_ALLOW_CREDENTIALS", "true").lower() in ("1", "true", "yes", "on")

    # Neo4j settings
    # NEO4J_URI: str = os.environ.get('NEO4J_URI', 'neo4j://127.0.0.1:7687')
    # NEO4J_USERNAME: str = os.environ.get('NEO4J_USERNAME', 'neo4j')
    # NEO4J_PASSWORD: str = os.environ.get('NEO4J_PASSWORD', 'password')

    # Oracle settings
    # ORACLE_USERNAME: str = os.environ.get('ORACLE_USERNAME', 'oracle')
    # ORACLE_PASSWORD: str = os.environ.get('ORACLE_PASSWORD', 'oracle')
    # ORACLE_HOST: str = os.environ.get('ORACLE_HOST', '127.0.0.1')
    # ORACLE_PORT: int = int(os.environ.get('ORACLE_PORT', '1521'))
    # ORACLE_SERVICE: str = os.environ.get('ORACLE_SERVICE', 'ORCLCDB.localdomain')
    # ORACLE_POOL_SIZE: int = int(os.environ.get('ORACLE_POOL_SIZE', '5'))
    # ORACLE_MAX_OVERFLOW: int = int(os.environ.get('ORACLE_MAX_OVERFLOW', '10'))

    # Authentication settings
    # AUTH_JWKS_BASE_URL: str = os.environ.get('AUTH_JWKS_BASE_URL', 'https://desapi-admin-ia.bdp.com.bo')
    # AUTH_JWT_ALGORITHMS: List[str] = os.environ.get('AUTH_JWT_ALGORITHMS', 'RS256').split(',')
    # AUTH_JWT_AUDIENCE: Optional[str] = os.environ.get('AUTH_JWT_AUDIENCE', 'SYS-CLI360')
    # AUTH_JWT_ISSUER: Optional[str] = os.environ.get('AUTH_JWT_ISSUER', 'https://desapi-admin-ia.bdp.com.bo')

    # LOGS
    LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
    LOG_FILE_PATH = Path(os.environ.get("LOG_FILE_PATH", str(LOG_DIR / "app.log")))
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
    MAX_LOG_FILE_SIZE = int(os.environ.get("LOG_MAX_BYTES", 10 * 1024 * 1024))
    LOG_BACKUP_COUNT = int(os.environ.get("LOG_BACKUP_COUNT", 5))

    # ElevenLabs
    ELEVENLABS_API_KEY: str = os.environ.get("ELEVENLABS_API_KEY", "")
    ELEVENLABS_API_URL: str = os.environ.get("ELEVENLABS_API_URL", "https://api.elevenlabs.io/v1")
    ELEVENLABS_VOICE_ID: str = os.environ.get("ELEVENLABS_VOICE_ID", "")
    ELEVENLABS_MODEL: str = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
    ELEVENLABS_TIMEOUT: int = int(os.environ.get("ELEVENLABS_TIMEOUT", "30"))


settings = Settings()
