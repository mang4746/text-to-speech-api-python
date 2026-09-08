# Lógica de negocio del módulo de autenticación
# Funciones que procesan datos de autenticación y errores

# from datetime import datetime
# from typing import Dict, Optional
# 
# from app.core.logger import get_logger
# from app.shared.exceptions import ValidationError
# from . import repository
# from .schema import LogError
# 
# logger = get_logger(__name__)
# 
# 
# async def get_current_user_info(current_user: dict) -> Dict:
#     """ Extrae y formatea información del usuario autenticado. """
#     try:
#         # Extraer timestamp actual para cálculos
#         current_timestamp = int(datetime.now().timestamp())
#         
#         # Calcular segundos restantes del token
#         exp_timestamp = current_user.get("exp", 0)
#         remaining_seconds = exp_timestamp - current_timestamp
#         
#         # Estructurar respuesta con información completa
#         user_info = {
#             "sub": current_user.get("sub"),                          # ID único del usuario
#             "sec_persona": current_user.get("sec_persona"),          # ID único de la persona
#             "roles": current_user.get("roles", []),                  # Lista de roles
#             "user": current_user.get("user"),                        # Info del usuario
#             "iat": current_user.get("iat"),                          # Timestamp emisión
#             "exp": current_user.get("exp"),                          # Timestamp expiración
#             "token_expires_in_seconds": max(0, remaining_seconds),   # Segundos para expirar
#             "aud": current_user.get("aud"),                          # Audiencia
#             "iss": current_user.get("iss"),                          # Emisor
#         }
#         
#         logger.debug(f"Información de usuario extraída: {current_user.get('sub')}")
#         return user_info
#         
#     except Exception as e:
#         logger.error(f"Error extrayendo información del usuario: {str(e)}")
#         raise
# 
# 
# async def validate_user_status(user_info: dict) -> bool:
#     """ Valida que el usuario esté en un estado válido para operar (ACTIVO). """
#     try:
#         # Obtener estado del usuario
#         user_status = user_info.get("user", {}).get("estado", "").upper()
#         
#         # Validar que usuario está ACTIVO
#         if user_status != "ACTIVO":
#             logger.warning(f"Usuario inactivo: {user_info.get('sub')}, estado: {user_status}")
#             return False
#         
#         # Validar que tiene al menos un rol ACTIVO
#         roles = user_info.get("roles", [])
#         has_active_role = any(role.get("estado", "").upper() == "ACTIVO" for role in roles)
#         
#         if not has_active_role:
#             logger.warning(f"Usuario sin roles activos: {user_info.get('sub')}")
#             return False
#         
#         logger.debug(f"Usuario validado: {user_info.get('sub')}")
#         return True
#         
#     except Exception as e:
#         logger.error(f"Error validando estado del usuario: {str(e)}")
#         return False
# 
# 
# async def create_log_error(log_error: LogError):
#     try:        
#         datos = await repository.create_log_error(log_error)
#         
#         if not datos:
#             raise ValidationError("No se pudo crear el log de error")
# 
#         return datos
#         
#     except Exception as e:
#         logger.error(f"Error al crear log de error: {str(e)}")
#         raise    