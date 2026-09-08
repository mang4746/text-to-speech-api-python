from typing import Dict

from app.core.config import settings
from app.core.logger import get_logger

# from app.db.neo4j.session import get_neo4j_driver
# import app.db.oracle.session as oracle_session
# from sqlalchemy import text

logger = get_logger(__name__)


async def get_health_status() -> Dict[str, str]:

    #neo4j_status = "UNAVAILABLE"
#
    #try:
    #    # Verificar conexión a Neo4j
    #    async with get_neo4j_driver().session() as session:
    #        result = await session.run("RETURN 1 AS test")
    #        await result.single()
    #        neo4j_status = "CONNECTED"
    #except Exception as e:
    #    logger.warning(f"Comprobación fallida de estado de Neo4j: {str(e)}")
    #    neo4j_status = "DISCONNECTED"
#
    ## Verificar conexión a Oracle
    #oracle_status = "UNAVAILABLE"
#
    #try:
    #    if oracle_session._oracle_sessionmaker is not None:
    #        logger.debug("Intentando conectar a Oracle para comprobación de salud...")
    #        async with oracle_session._oracle_sessionmaker() as session:
    #            result = await session.execute(text("SELECT 1 FROM DUAL"))
    #            result.scalar_one()
    #            oracle_status = "CONNECTED"
    #    else:
    #        oracle_status = "NOT INITIALIZED"
    #except Exception as e:
    #    logger.warning(f"Comprobación fallida de estado de Oracle: {str(e)}")
    #    oracle_status = "DISCONNECTED"

    # Determinar estado general
    # overall_status = "UP" if neo4j_status == "CONNECTED" and oracle_status == "CONNECTED" else "DEGRADED"

    overall_status = "UP"

    return {
        "status": overall_status,
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "log_level": settings.LOG_LEVEL,
        # "neo4j_status": neo4j_status,
        # "oracle_status": oracle_status,
    }
