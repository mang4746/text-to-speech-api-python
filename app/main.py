from fastapi import FastAPI, Request
# from Rutas import EndPointsAuth , EndPointsClientes , EndPointsCreditos , EndPointsAdi, EndPointGerencial, EndPointsAdministration , EndPointsGemeloToCRM
# from Scripts.Auth import get_current_user
# from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import get_logger, setup_logger

from app.api.v1.routers import router as api_v1_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.banner import print_banner
from app.shared.factories.response_factory import ResponseFactory
# from app.db.neo4j.session import initialize_neo4j_driver, close_neo4j_driver
# from app.db.oracle.session import initialize_oracle_engine, close_oracle_engine

setup_logger()
logger = get_logger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url=settings.APP_DOCS_URL,
    redoc_url=settings.APP_REDOC_URL,
    # openapi_tags=tags_metadata
)

# Registrar manejadores globales de excepciones
register_exception_handlers(app)


@app.on_event("startup")
async def startup_event():
    print_banner()
    # Inicializar drivers y conexiones cuando la aplicación inicia
    # logger.info("Inicializando Neo4j driver...")
    # initialize_neo4j_driver()
    # logger.info("Inicializando Oracle engine...")
    # initialize_oracle_engine()


@app.on_event("shutdown")
async def shutdown_event():
    # Cerrar conexiones cuando la aplicación se detiene
    # logger.info("Cerrando Oracle engine...")
    # await close_oracle_engine()
    # await close_neo4j_driver()
    logger.info("Aplicación cerrada correctamente.")

# client = TestClient(app)

# CORS: Permitir solicitudes desde cualquier origen (ajustar en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
    expose_headers=["*"],
)

# Middleware para capturar el request en el contexto de ResponseFactory, para obtener el path
@app.middleware("http")
async def set_request_context(request: Request, call_next):
    ResponseFactory.set_request(request)
    response = await call_next(request)
    return response

app.include_router(
    api_v1_router,
    prefix="/api/v1"
)
