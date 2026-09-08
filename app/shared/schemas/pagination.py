"""Esquemas de paginación."""

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Información de paginación."""
    total: int = Field(..., description="Total de registros")
    per_page: int = Field(..., description="Registros por página")
    current_page: int = Field(..., description="Página actual")
    last_page: int = Field(..., description="Última página")
    from_: int = Field(..., alias="from", description="Desde registro")
    to: int = Field(..., description="Hasta registro")

    class Config:
        populate_by_name = True
