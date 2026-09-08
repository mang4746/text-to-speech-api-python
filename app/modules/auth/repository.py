# Capa de Acceso a Datos - Auth
# Responsable de ejecutar queries a Neo4j y transformar resultados

# from typing import Optional, Dict, Any, List
# from app.db.neo4j.session import get_neo4j_driver
# 
# from app.core.logger import get_logger
# from .schema import LogError
# 
# logger = get_logger(__name__)
# 
# 
# async def create_log_error(log_error: LogError) -> Optional[Dict[str, Any]]:
#     try:
#         async with get_neo4j_driver().session() as session:
#             result = await session.run(
#                 query="""
#                     CREATE (p:LogErrores) 
#                     SET p.id = apoc.create.uuid() , p.usuario = $usuario, p.Error = $error, p.origen = $origen , p.fechaError = datetime()
#                     RETURN p
#                 """,
#                 parameters={
#                     'usuario': log_error.usuario,
#                     'error': log_error.error,
#                     'origen': log_error.origen
#                 }
#             )            
#             record = await result.single()
#             
#             if not record:
#                 return None
#             
#             # Transformar resultado a diccionario
#             data = record.data()
#             return data
#             
#     except Exception as e:
#         logger.error(f"Error al crear log de error: {str(e)}")
#         raise