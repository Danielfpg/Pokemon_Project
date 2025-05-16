import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(dotenv_path="variables.env")

Base = declarative_base ()

USER = os.getenv('CLEVER_USER')
PASSWORD = os.getenv('CLEVER_PASSWORD')
HOST = os.getenv('CLEVER_HOST')
PORT = os.getenv('CLEVER_PORT')
DB_NAME = os.getenv('CLEVER_DATABASE')

if all([USER, PASSWORD, HOST, PORT, DB_NAME]):

    DB_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
else:
    print("⚠️ Variables de entorno incompletas. Usando SQLite por defecto.")
    DB_URL = "sqlite+aiosqlite:///Pokemondb.db"

engine = create_async_engine(DB_URL, echo=True)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Error al crear las tablas: {e}")


async def get_session():
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        print(f"Error al obtener la sesión: {e}")
        raise
