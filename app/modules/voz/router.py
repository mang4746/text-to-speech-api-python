from fastapi import APIRouter

from app.shared.factories.response_factory import ResponseFactory
from app.shared.schemas.response import ApiResponse

# from typing_extensions import Annotated
# from app.core.dependencies import get_current_user
from . import service
from .schema import TextRequest

router = APIRouter()

@router.post(
    "/generate",
    response_model=ApiResponse,
    summary="Generar voz a partir de texto",
    description="Endpoint para generar voz a partir de texto."
)
async def generate_voz(
    request: TextRequest,
):
    # Endpoint para generar voz a partir de texto
    resp = await service.generate_voz(request.text)
    
    # Retorna respuesta estandarizada
    return ResponseFactory.success(
        data=resp,
        code=200,
        message="Voz generada correctamente"
    )
