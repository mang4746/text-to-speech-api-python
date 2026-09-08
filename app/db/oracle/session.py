#from typing import AsyncGenerator, Optional
#
#from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
#from app.core.config import settings
#from app.core.logger import get_logger
#
#logger = get_logger(__name__)
#
#_oracle_engine: Optional[AsyncEngine] = None
#_oracle_sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None
#
#
#def _build_oracle_url() -> str:
#    return (
#        f"oracle+oracledb://{settings.ORACLE_USERNAME}:"
#        f"{settings.ORACLE_PASSWORD}@{settings.ORACLE_HOST}:"
#        f"{settings.ORACLE_PORT}/?service_name={settings.ORACLE_SERVICE}"
#    )
#
#
#def initialize_oracle_engine() -> AsyncEngine:
#    """Inicializa el engine de Oracle y el sessionmaker."""
#    global _oracle_engine, _oracle_sessionmaker
#
#    if _oracle_engine is not None:
#        return _oracle_engine
#
#    oracle_url = _build_oracle_url()
#    _oracle_engine = create_async_engine(
#        oracle_url,
#        echo=False,
#        future=True,
#        pool_size=settings.ORACLE_POOL_SIZE,
#        max_overflow=settings.ORACLE_MAX_OVERFLOW,
#        # connect_args={
#        #     "encoding": "UTF-8",
#        #     "nencoding": "UTF-8",
#        # },
#    )
#
#    _oracle_sessionmaker = async_sessionmaker(
#        bind=_oracle_engine,
#        expire_on_commit=False,
#        class_=AsyncSession,
#    )
#
#    logger.info("Oracle engine inicializado correctamente: %s", oracle_url)
#    return _oracle_engine
#
#
#async def close_oracle_engine() -> None:
#    """Cierra el engine de Oracle al apagar la aplicación."""
#    global _oracle_engine
#
#    if _oracle_engine is not None:
#        logger.info("Cerrando Oracle engine...")
#        await _oracle_engine.dispose()
#        _oracle_engine = None
#
#
#async def get_oracle_session() -> AsyncGenerator[AsyncSession, None]:
#    """Dependencia FastAPI que provee una sesión Oracle por request."""
#    if _oracle_sessionmaker is None:
#        raise RuntimeError("El engine de Oracle no ha sido inicializado.")
#
#    async with _oracle_sessionmaker() as session:
#        yield session
#