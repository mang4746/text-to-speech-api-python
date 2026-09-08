# Definición de roles y permisos disponibles en la aplicación
# Estructura centralizada para validación de acceso por rol

from enum import Enum


class UserRole(str, Enum):
    """Roles disponibles en el sistema."""
    # Administrativos
    ADMINISTRADOR = "ADM"                     # Administrador del Sistema
    ADMINISTRADOR_USUARIOS = "AUS"            # Administrador de Usuarios
    
    # Operacionales
    GERENCIAL = "GER"               # Gerente
    JEFE_AGENCIA = "JAG"            # Jefe de Agencia
    OFICIAL_CREDITO = "OFC"         # Oficial de Crédito


# Descripción de roles para documentación
ROLE_DESCRIPTIONS = {
    UserRole.ADMINISTRADOR: "Administrador del Sistema",
    UserRole.ADMINISTRADOR_USUARIOS: "Administrador de Usuarios - Gestiona usuarios y permisos",
    UserRole.OFICIAL_CREDITO: "Oficial de Crédito - Gestiona clientes y créditos",
    UserRole.JEFE_AGENCIA: "Jefe de Agencia - Supervisa operaciones y personal",
    UserRole.GERENCIAL: "Gerente - Acceso a reportes y análisis gerenciales",
}


# Permisos por rol (define qué puede hacer cada rol)
ROLE_PERMISSIONS = {
    UserRole.ADMINISTRADOR: [
        "view_all",
        "manage_users",
        "manage_roles",
        "view_system_logs",
        "configure_system",
    ],
    UserRole.OFICIAL_CREDITO: [
        "view_clients",
        "view_credits",
        "view_own_portfolio",
        "view_dashboard",
    ],
    UserRole.JEFE_AGENCIA: [
        "view_clients",
        "view_credits",
        "view_own_portfolio",
        "view_dashboard",
    ],
    UserRole.GERENCIAL: [
        "view_clients",
        "view_credits",
        "view_own_portfolio",
        "view_dashboard",
    ],
}


# Mensajes de error estándar
ERROR_MESSAGES = {
    # AUTH / SECURITY
    "invalid_token": "Token inválido o expirado",
    "missing_token": "Token no proporcionado",
    "insufficient_role": "Rol insuficiente para acceder a este recurso",
    "role_not_found": "Rol del usuario no está configurado",
    "user_inactive": "Usuario inactivo",
    "access_denied": "Acceso denegado",
    "unauthorized": "No autorizado",

    # API Key
    "invalid_api_key": "API Key inválida",
    "missing_api_key": "API Key no proporcionada",

    # VALIDATION
    "validation_error": "Error de validación",
    "invalid_payload": "Datos enviados no válidos",
    "missing_required_fields": "Faltan campos obligatorios",
    "invalid_path_param": "Parámetro de ruta inválido",
    "invalid_query_param": "Parámetro de consulta inválido",

    # CRUD / RESOURCES
    "resource_not_found": "Recurso no encontrado",
    "resource_already_exists": "El recurso ya existe",
    "resource_conflict": "Conflicto con el recurso solicitado",
    "cannot_delete_resource": "No se puede eliminar el recurso",
    "resource_in_use": "El recurso está en uso",

    # GET
    "data_not_found": "No se encontraron datos",
    "empty_result": "Sin resultados",

    # POST
    "create_failed": "No se pudo crear el recurso",
    "duplicate_record": "Registro duplicado",

    # PUT / PATCH
    "update_failed": "No se pudo actualizar el recurso",
    "nothing_to_update": "No hay cambios para actualizar",

    # DELETE
    "delete_failed": "No se pudo eliminar el recurso",
    "already_deleted": "El recurso ya fue eliminado",

    # SERVER / INFRA
    "internal_error": "Error interno del servidor",
    "database_error": "Error en base de datos",
    "neo4j_error": "Error procesando consulta Neo4j",
    "service_unavailable": "Servicio no disponible",
    "timeout": "Tiempo de espera agotado",

    # EXTERNAL SERVICES
    "ldap_error": "Error en servicio de autenticación LDAP",
    "jwks_error": "Error obteniendo claves de autenticación",
    "integration_error": "Error en servicio externo",
}


# Estados posibles de usuarios
class UserStatus(str, Enum):
    """Estados posibles de un usuario."""
    ACTIVE = "ACTIVO"
    INACTIVE = "INACTIVO"
    SUSPENDED = "SUSPENDIDO"