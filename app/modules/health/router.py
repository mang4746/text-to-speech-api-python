from fastapi import APIRouter, Depends
# from typing_extensions import Annotated

# from app.core.dependencies import get_current_user
from app.core.auth.api_key import validate_api_key
from . import service
from app.shared.factories.response_factory import ResponseFactory
from app.shared.schemas.response import ApiResponse

router = APIRouter()

@router.get(
    "/health",
    response_model=ApiResponse,
    summary="Verificar estado del servicio",
    description="Endpoint público para comprobar que el servicio está disponible."
)
async def health_check():
    status = await service.get_health_status()
    
    # Retorna respuesta estandarizada
    return ResponseFactory.success(
        data=status,
        code=200,
        message="Servicio disponible"
    )


@router.get(
    "/health/secure",
    response_model=ApiResponse,
    summary="Verificar estado del servicio con autenticación",
    description="Endpoint protegido que valida el API Key y verifica el estado del servicio.",
    dependencies=[Depends(validate_api_key)]
)
async def health_check_secure():
    status = await service.get_health_status()
    
    # Retorna respuesta estandarizada
    return ResponseFactory.success(
        data=status,
        code=200,
        message="Servicio disponible y API Key válido"
    )