from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connection import init_db, get_session
from db.db_Operations_Pokemon_Card import *
from db.db_Operations_Energie_Card import *
from db.db_Operations_Trainer_Card import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "¡Bienvenido al sistema de cartas!"}

# ---------- POKEMON ----------

@app.post("/cartas/pokemon")
async def crear_carta_pokemon():
    return await crear_carta_pokemon(db, nombre, rare, costo_en_bolsa, tipo, stats_id)

@app.get("/cartas/pokemon/{pokemon_id}")
async def obtener_carta_pokemon(pokemon_id: int, db: AsyncSession = Depends(get_session)):
    carta = await db_get_carta_pokemon(db, pokemon_id)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return carta

@app.get("/cartas/pokemon")
async def obtener_cartas_pokemon(db: AsyncSession = Depends(get_session)):
    return await db_get_all_cartas_pokemon(db)

@app.delete("/cartas/pokemon/{pokemon_id}")
async def eliminar_carta_pokemon(pokemon_id: int, db: AsyncSession = Depends(get_session)):
    carta_eliminada = await db_delete_carta_pokemon(db, pokemon_id)
    if not carta_eliminada:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return {"message": "Carta Pokémon eliminada y respaldada"}

# ---------- ENERGÍA ----------

@app.post("/cartas/energia")
async def crear_carta_energia(
    nombre: str, rare: str, costo_en_bolsa: float, tipo: str, especial: bool, db: AsyncSession = Depends(get_session)
):
    return await db_create_carta_energia(db, nombre, rare, costo_en_bolsa, tipo, especial)

@app.get("/cartas/energia/{energia_id}")
async def obtener_carta_energia(energia_id: int, db: AsyncSession = Depends(get_session)):
    carta = await db_get_carta_energia(db, energia_id)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta de Energía no encontrada")
    return carta

@app.get("/cartas/energia")
async def obtener_cartas_energia(db: AsyncSession = Depends(get_session)):
    return await db_get_all_cartas_energia(db)

@app.delete("/cartas/energia/{energia_id}")
async def eliminar_carta_energia(energia_id: int, db: AsyncSession = Depends(get_session)):
    carta_eliminada = await db_delete_carta_energia(db, energia_id)
    if not carta_eliminada:
        raise HTTPException(status_code=404, detail="Carta de Energía no encontrada")
    return {"message": "Carta de Energía eliminada y respaldada"}

# ---------- ENTRENADOR ----------

@app.post("/cartas/entrenador")
async def crear_carta_entrenador(
    subtipo: str, efecto: str, tiempo: str, db: AsyncSession = Depends(get_session)
):
    return await db_create_carta_entrenador(db, subtipo, efecto, tiempo)

@app.get("/cartas/entrenador/{entrenador_id}")
async def obtener_carta_entrenador(entrenador_id: int, db: AsyncSession = Depends(get_session)):
    carta = await db_get_carta_entrenador(db, entrenador_id)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta de Entrenador no encontrada")
    return carta

@app.get("/cartas/entrenador")
async def obtener_cartas_entrenador(db: AsyncSession = Depends(get_session)):
    return await db_get_all_cartas_entrenador(db)

@app.delete("/cartas/entrenador/{entrenador_id}")
async def eliminar_carta_entrenador(entrenador_id: int, db: AsyncSession = Depends(get_session)):
    carta_eliminada = await db_delete_carta_entrenador(db, entrenador_id)
    if not carta_eliminada:
        raise HTTPException(status_code=404, detail="Carta de Entrenador no encontrada")
    return {"message": "Carta de Entrenador eliminada y respaldada"}
