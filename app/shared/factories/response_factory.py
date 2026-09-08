"""Factory para construir respuestas HTTP estándar."""

from typing import Optional, TypeVar, Any
from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from fastapi import Request
from contextvars import ContextVar

from app.shared.schemas.response import ApiResponse, ApiMeta
from app.shared.schemas.pagination import Pagination

T = TypeVar("T")

# Context var para almacenar el request actual
request_context: ContextVar[Optional[Request]] = ContextVar('request', default=None)


class ResponseFactory:
    """Factory pattern para construir respuestas estándar de la API."""

    @staticmethod
    def set_request(request: Request) -> None:
        """Establece el request actual en el contexto."""
        request_context.set(request)

    @staticmethod
    def _get_path() -> Optional[str]:
        """Obtiene automáticamente el path del request actual."""
        request = request_context.get()
        return request.url.path if request else None

    @staticmethod
    def success(
        data: Optional[T] = None,
        code: int = 200,
        message: str = "Operación exitosa",
        path: Optional[str] = None,
        pagination: Optional[Pagination] = None,
    ) -> JSONResponse:
        """Construye una respuesta exitosa."""
        # Usar path automático si no se proporciona
        final_path = path or ResponseFactory._get_path()
        
        # Crear metadata si tenemos un path válido
        meta = None
        if final_path:
            meta = ApiMeta(
                timestamp=datetime.now(timezone.utc).isoformat(),
                path=final_path,
                pagination=pagination
            )

        # Construir respuesta
        response = ApiResponse(
            success=True,
            code=code,
            message=message,
            data=data,
            errors=None,
            meta=meta
        )

        # Retornar JSONResponse directamente
        return JSONResponse(
            status_code=code,
            content=response.model_dump(exclude_none=False)
            # content=response.model_dump(exclude_none=True)
        )

    @staticmethod
    def error(
        code: int = 400,
        message: str = "Error en la solicitud",
        errors: Optional[dict] = None,
        path: Optional[str] = None,
    ) -> JSONResponse:
        """Construye una respuesta de error."""
        # Usar path automático si no se proporciona
        final_path = path or ResponseFactory._get_path()
        
        # Crear metadata si tenemos un path válido
        meta = None
        if final_path:
            meta = ApiMeta(
                timestamp=datetime.now(timezone.utc).isoformat(),
                path=final_path
            )

        # Construir respuesta
        response = ApiResponse(
            success=False,
            code=code,
            message=message,
            data=None,
            errors=errors,
            meta=meta
        )

        # Retornar JSONResponse directamente
        return JSONResponse(
            status_code=code,
            content=response.model_dump(exclude_none=True)
        )

    @staticmethod
    def paginated(
        data: list,
        total: int,
        per_page: int,
        current_page: int,
        code: int = 200,
        message: str = "Listado paginado",
        path: Optional[str] = None,
    ) -> JSONResponse:
        """Construye una respuesta con datos paginados."""
        # Calcular información de paginación
        last_page = (total + per_page - 1) // per_page
        from_record = (current_page - 1) * per_page + 1
        to_record = min(current_page * per_page, total)

        # Crear objeto de paginación
        pagination = Pagination(
            total=total,
            per_page=per_page,
            current_page=current_page,
            last_page=last_page,
            from_=from_record,
            to=to_record
        )

        # Usar path automático si no se proporciona
        final_path = path or ResponseFactory._get_path() or "/"
        
        # Crear metadata
        meta = ApiMeta(
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=final_path,
            pagination=pagination
        )

        # Construir respuesta paginada
        response = ApiResponse(
            success=True,
            code=code,
            message=message,
            data=data,
            errors=None,
            meta=meta
        )

        # Retornar JSONResponse directamente
        return JSONResponse(
            status_code=code,
            content=response.model_dump(exclude_none=True)
        )
