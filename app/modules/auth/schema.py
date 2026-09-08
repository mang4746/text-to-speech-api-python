# Modelos Pydantic para el módulo de autenticación
# Define estructuras de solicitud y respuesta

# from datetime import datetime
# from typing import Optional, List
# from pydantic import BaseModel, Field
# 
# 
# class Rol(BaseModel):
#     """Información de un rol del usuario."""
#     # Código único del rol (ej: OFC, ADM, GER)
#     cod_rol: str = Field(..., description="Código del rol")
#     # Nombre descriptivo del rol
#     nombre: str = Field(..., description="Nombre del rol")
#     # Estado actual del rol (ACTIVO, INACTIVO)
#     estado: str = Field(..., description="Estado del rol")
#     # Descripción del rol
#     descripcion: Optional[str] = Field(None, description="Descripción del rol")
#     # Fecha de creación del rol
#     fecha_creacion: Optional[datetime] = Field(None, description="Fecha de creación")
# 
# 
# class User(BaseModel):
#     """Información del usuario."""
#     # Login/identificador único del usuario
#     login: str = Field(..., description="Login del usuario")
#     # Nombre completo del usuario
#     nombre_usuario: str = Field(..., description="Nombre completo")
#     # Email del usuario
#     email: Optional[str] = Field(None, description="Email del usuario")
#     # Cargo/posición del usuario
#     cargo: Optional[str] = Field(None, description="Cargo del usuario")
#     # Estado actual (ACTIVO, INACTIVO, SUSPENDIDO)
#     estado: str = Field(..., description="Estado del usuario")
# 
# 
# class CurrentUser(BaseModel):
#     """Respuesta con información del usuario autenticado actual."""
#     # Identificador único del usuario (sub del JWT)
#     sub: str = Field(..., description="Identificador del usuario")
#     # Lista de roles asignados al usuario
#     roles: List[Rol] = Field(default_factory=list, description="Roles del usuario")
#     # Información del usuario
#     user: User = Field(..., description="Datos del usuario")
#     # Timestamps del token
#     iat: int = Field(..., description="Issued at (en Unix timestamp)")
#     exp: int = Field(..., description="Expiration time (en Unix timestamp)")
#     # Audiencia del token (para qué sistema es)
#     aud: Optional[str] = Field(None, description="Audiencia del token")
#     # Emisor del token
#     iss: Optional[str] = Field(None, description="Emisor del token")
# 
# 
# class LogError(BaseModel):
#     usuario: str = Field(..., description="Usuario que generó el error")
#     error: str = Field(..., description="Mensaje de error")
#     origen: str = Field(..., description="Origen del error (ej: API, Servicio externo)")
#     
#     model_config = {
#         "json_schema_extra": {
#             "examples": [
#                 {
#                     "usuario": "MISOTO",
#                     "error": "Error al procesar solicitud",
#                     "origen": "API"
#                 }
#             ]
#         }
#     }