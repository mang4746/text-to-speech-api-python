# Endpoints del módulo de autenticación
# Rutas para obtener información del usuario y registrar errores

# from typing import Annotated
# from fastapi import APIRouter, Depends
# 
# from app.core.logger import get_logger
# from app.core.auth.dependencies import get_current_user
# from app.shared.factories.response_factory import ResponseFactory
# from app.shared.schemas.response import ApiResponse
# from .schema import LogError
# from . import service
# 
# logger = get_logger(__name__)
# 
# # Crear router para este módulo
# router = APIRouter()
# 
# 
# @router.get(
#     "/me",
#     response_model=ApiResponse,
#     summary="Obtener datos del usuario autenticado",
#     description="""
#         Retorna la información completa del usuario actualmente autenticado
#         \n\n**Roles:** Todos
#     """
# )
# async def get_current_user(
#     current_user: Annotated[dict, Depends(get_current_user)]
# ):
#     """
#     Obtiene información del usuario autenticado actual.
#     Ruta anterior: POST /cliente360/auth/user_data_login
#     """
#     try:
#         # Procesar y formatear información del usuario
#         user_info = await service.get_current_user_info(current_user)
#         
#         # Validar que el usuario está en estado válido
#         is_valid = await service.validate_user_status(current_user)
#         if not is_valid:
#             logger.warning(f"Usuario inválido intentó acceder: {current_user.get('sub')}")
#             return ResponseFactory.error(
#                 code=403,
#                 message="Usuario inactivo o sin roles válidos",
#                 path="/auth/me"
#             )
#         
#         # Retornar respuesta exitosa con información del usuario
#         return ResponseFactory.success(
#             data=user_info,
#             code=200,
#             message="Información del usuario obtenida correctamente"
#         )
#         
#     except Exception as e:
#         logger.error(f"Error obteniendo información del usuario: {str(e)}")
#         return ResponseFactory.error(
#             code=500,
#             message="Error al obtener información del usuario",
#             path="/auth/me"
#         )
#     
# 
# @router.post(
#     "/log-error",
#     response_model=ApiResponse,
#     summary="Crear log de error | Antes: POST /cliente360/auth/log-error/",
#     description="""
#         Guarda log de errores
#         \n\n**Roles:** Todos
#         \n\n**Ruta migrada de:** POST /cliente360/auth/log-error/
#     """
# )
# async def create_log_error(
#     current_user: Annotated[dict, Depends(get_current_user)],
#     request: LogError
# ):
#     datos = await service.create_log_error(request)
#     
#     return ResponseFactory.success(
#         data=datos,
#         code=201,
#         message="Log de error creado exitosamente",
#     )