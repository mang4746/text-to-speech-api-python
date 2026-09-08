"""Excepciones personalizadas de la aplicación."""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Excepción base de la aplicación."""
    pass


class NotFoundError(AppException):
    """Recurso no encontrado (404)."""
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )


class ValidationError(AppException):
    """Error de validación (422)."""
    def __init__(self, message: str = "Validación fallida"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )


class UnauthorizedError(AppException):
    """No autorizado (401)."""
    def __init__(self, message: str = "No autorizado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )


class ForbiddenError(AppException):
    """Acceso prohibido (403)."""
    def __init__(self, message: str = "Acceso prohibido"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class ForbiddenRoleError(AppException):
    """Rol insuficiente para acceder al recurso (403)."""
    def __init__(self, message: str = "Rol insuficiente para acceder a este recurso"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class ConflictError(AppException):
    """Conflicto (409)."""
    def __init__(self, message: str = "Conflicto"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class InternalServerError(AppException):
    """Error interno del servidor (500)."""
    def __init__(self, message: str = "Error interno del servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )


# Excepciones específicas para autenticación JWT
class TokenExpiredError(UnauthorizedError):
    """Token JWT expirado (401)."""
    def __init__(self, message: str = "Token expirado"):
        super().__init__(message)


class TokenInvalidError(UnauthorizedError):
    """Token JWT inválido (401)."""
    def __init__(self, message: str = "Token inválido"):
        super().__init__(message)


class CredentialsError(UnauthorizedError):
    """Credenciales inválidas (401)."""
    def __init__(self, message: str = "Credenciales inválidas"):
        super().__init__(message)


