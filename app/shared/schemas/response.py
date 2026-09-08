"""Esquemas de respuesta estándar de la API."""

from typing import Generic, TypeVar, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.shared.schemas.pagination import Pagination

T = TypeVar("T")

# Metadata de la respuesta API
class ApiMeta(BaseModel):
    """Información adicional de la respuesta."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    path: str = Field(..., description="Ruta solicitada")
    pagination: Optional[Pagination] = Field(None, description="Info de paginación")

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2026-04-20T12:00:00.000000",
                "path": "/api/users",
                "pagination": None
            }
        }


# Respuesta estándar genérica
class ApiResponse(BaseModel, Generic[T]):
    """Estructura estándar de respuesta HTTP de la API."""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    code: int = Field(..., description="Código HTTP")
    message: str = Field(..., description="Mensaje descriptivo")
    data: Optional[T] = Field(None, description="Datos de la respuesta")
    errors: Optional[dict] = Field(None, description="Detalles de errores si aplica")
    meta: Optional[ApiMeta] = Field(None, description="Metadata adicional")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "code": 200,
                "message": "Operación exitosa",
                "data": {},
                "errors": None,
                "meta": {
                    "timestamp": "2026-04-20T12:00:00",
                    "path": "/api/users",
                    "pagination": None
                }
            }
        }
