from fastapi import APIRouter

# Importar routers de todos los módulos
from app.modules.health.router import router as health_router
# from app.modules.auth.router import router as auth_router
from app.modules.voz.router import router as voz_router
from app.modules.voz_stream.router import router as voz_stream_router

# Crear router principal v1
router = APIRouter()

# Incluir routers de todos los módulos con prefijos apropiados
router.include_router(health_router, prefix="", tags=["Health"])
# router.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
router.include_router(voz_router, prefix="/voz", tags=["Generación de Voz"])
router.include_router(voz_stream_router, prefix="/voz-stream", tags=["Generación de Voz por Streaming"])

__all__ = ["router"]
