# Modelos Pydantic para Requests de los Endpoints

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class IntervaloFechasRequest(BaseModel):
    fecha_ini: date = Field(..., description="Fecha inicial")
    fecha_fin: date = Field(..., description="Fecha final")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "fecha_ini": "2026-01-01",
                    "fecha_fin": "2026-04-22"
                }
            ]
        }
    }


class PaginationRequest(BaseModel):
    """Request con paginación y búsqueda avanzada"""
    page: int = Field(1, ge=1, description="Número de página (1-indexado)")
    size: int = Field(10, ge=1, le=100, description="Elementos por página (máx 100)")
    # search: str = Field("", description="Término de búsqueda (búsqueda avanzada en múltiples campos)")
    search: Optional[str] = Field(None, description="Término de búsqueda (búsqueda en múltiples campos)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "page": 1,
                    "size": 10,
                    "search": "Buscar..."
                }
            ]
        }
    }