from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./cartas.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Crear el sessionmaker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)

# Función para obtener la sesión de la base de datos
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
