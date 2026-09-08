"""Manejadores globales de excepciones."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from app.shared.factories.response_factory import ResponseFactory
from app.shared.exceptions import AppException, NotFoundError
from app.core.constants import ERROR_MESSAGES


# Manejador para excepciones personalizadas de la aplicación
async def app_exception_handler(request: Request, exc: AppException):
    """Maneja excepciones personalizadas de la aplicación."""
    return ResponseFactory.error(
        code=exc.status_code,
        message=exc.detail,
        path=str(request.url.path)
    )


# Manejador para errores de validación de Pydantic
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic."""
    # Construir diccionario de errores por campo
    errors = {}
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])
        errors[field] = error["msg"]
    
    return ResponseFactory.error(
        code=422,
        message= ERROR_MESSAGES["validation_error"],
        errors=errors,
        path=str(request.url.path)
    )


# Manejador excepciones de Not Found (404)
async def not_found_handler(request: Request, exc: NotFoundError):
    raw_message = str(getattr(exc, "detail", "")).strip()

    if not raw_message or raw_message.lower() == "not found":
        message = ERROR_MESSAGES["resource_not_found"]
    else:
        message = raw_message

    return ResponseFactory.error(
        code=404,
        message=message,
        path=str(request.url.path)
    )


# Manejador para excepciones genéricas
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones genéricas no capturadas."""
    # En producción, registrar el error en logs
    exc_detail = str(exc) if str(exc) else "Error desconocido"
    
    return ResponseFactory.error(
        code=500,
        message=ERROR_MESSAGES["internal_error"],
        errors={"detail": exc_detail},
        path=str(request.url.path)
    )


def register_exception_handlers(app: FastAPI):
    """Registra todos los exception handlers globales en la aplicación."""
    # Usar add_exception_handler en lugar de decoradores
    # Esto evita problemas de accesibilidad en Pylance
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(NotFoundError, not_found_handler)
    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(Exception, general_exception_handler)