# SQLAlchemy async engine and sessions tools
#
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
#
# for pool size configuration:
# https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.Pool

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings


def new_async_engine(uri: URL) -> AsyncEngine:
    return create_async_engine(
        uri,
        pool_pre_ping=True,  # Verifica que la conexión esté activa antes de usarla
        pool_size=1,  # SQLite solo permite una conexión de escritura a la vez
        max_overflow=0,  # Evita conexiones adicionales
        pool_timeout=30.0,  # Tiempo de espera para obtener una conexión
        pool_recycle=600,  # Recicla las conexiones después de 600 segundos
    )


# Crea el motor asíncrono usando la URL de la base de datos desde la configuración
_ASYNC_ENGINE = new_async_engine(get_settings().sqlalchemy_database_uri)

# Crea una fábrica de sesiones asíncronas
_ASYNC_SESSIONMAKER = async_sessionmaker(_ASYNC_ENGINE, expire_on_commit=False)


def get_async_session() -> AsyncSession:  # pragma: no cover
    return _ASYNC_SESSIONMAKER()
