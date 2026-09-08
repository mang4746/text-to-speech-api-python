#"""Neo4j database session and driver management.
#
#Proporciona acceso centralizado al driver de Neo4j con:
#- Singleton pattern: Una sola instancia del driver
#- Connection pooling: Manejado automáticamente por el driver
#- Lifecycle management: Inicialización en startup, cierre en shutdown
#- Async support: Compatible con async/await de FastAPI
#"""
#
#from typing import Optional
#from neo4j import  AsyncGraphDatabase
#from app.core.config import settings
#from app.core.logger import get_logger
#
#logger = get_logger(__name__)
#
## ============================================================================
## Neo4j Driver (Singleton)
## ============================================================================
#
## Variable global que mantiene la instancia del driver
#_neo4j_driver: Optional[object] = None
#
#
#def initialize_neo4j_driver() -> object:
#    """
#    Inicializa el driver de Neo4j.
#    
#    Se ejecuta en app.on_event("startup").
#    Usa AsyncGraphDatabase para soportar operaciones async.
#    
#    Returns:
#        Neo4j driver instance (AsyncDriver)
#        
#    Raises:
#        Exception: Si hay error de conexión
#        
#    MEJORES PRÁCTICAS:
#    - El driver es un singleton (una sola instancia)
#    - No cerrar el driver después de cada operación
#    - El driver maneja un pool de conexiones internamente
#    - Reutilizar el mismo driver para múltiples operaciones
#    """
#    global _neo4j_driver
#    
#    try:        
#        # Usar AsyncGraphDatabase para operaciones async
#        _neo4j_driver = AsyncGraphDatabase.driver(
#            settings.NEO4J_URI,
#            auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD),
#            # Configuraciones opcionales para mejor desempeño
#            connection_acquisition_timeout=30.0,  # Timeout para obtener conexión del pool
#            connection_timeout=30.0,  # Timeout para conectar al servidor
#            resolver=None,  # Usar DNS resolver por defecto
#        )
#        
#        logger.info("Neo4j driver inicializado correctamente en: %s", settings.NEO4J_URI)
#        return _neo4j_driver
#        
#    except Exception:
#        logger.exception("Error al inicializar Neo4j driver")
#        raise
#
#
#async def close_neo4j_driver():
#    """
#    Cierra la conexión del driver de Neo4j.
#    
#    Se ejecuta en app.on_event("shutdown").
#    Libera todas las conexiones del pool.
#    
#    MEJORES PRÁCTICAS:
#    - Llamar una sola vez al apagar la aplicación
#    - No llamar dentro de endpoints (el driver es un recurso global)
#    - Esperar a que se cierren todas las conexiones activas
#    """
#    global _neo4j_driver
#    
#    if _neo4j_driver:
#        try:
#            logger.info("Cerrando Neo4j driver...")
#            await _neo4j_driver.close()
#            _neo4j_driver = None
#            logger.info("Neo4j driver cerrado correctamente")
#        except Exception:
#            logger.exception("Error al cerrar Neo4j driver")
#            raise
#
#
#def get_neo4j_driver() -> object:
#    """
#    Obtiene la instancia del driver Neo4j.
#    
#    Returns:
#        Neo4j driver instance (AsyncDriver)
#        
#    Raises:
#        RuntimeError: Si el driver no ha sido inicializado
#        
#    USO:
#        from app.db.neo4j.session import get_neo4j_driver
#        
#        async with get_neo4j_driver().session() as session:
#            result = await session.run("MATCH (n) RETURN n LIMIT 1")
#            record = await result.single()
#    """
#    if _neo4j_driver is None:
#        raise RuntimeError(
#            "Neo4j driver no está inicializado. "
#            "Asegúrate de que el evento 'startup' fue ejecutado correctamente."
#        )
#    return _neo4j_driver
#
#
## Alias para compatibilidad y claridad
#neo4j_driver = property(lambda self: get_neo4j_driver())
#
#
## ============================================================================
## Exportaciones
## ============================================================================
#
#__all__ = [
#    "get_neo4j_driver",
#    "initialize_neo4j_driver",
#    "close_neo4j_driver",
#]
