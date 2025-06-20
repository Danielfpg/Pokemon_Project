from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from Models.Model_pydantic.Model_Pokemon_card import CartaPokemon
from Models.Model_pydantic.Model_Energie_card import CartaEnergia
from Models.Model_pydantic.Model_Trainer_card import CartaEntrenador
from Models.Model_pydantic.main_model_card import CartModel
from Models.Model_db.Pokemon_Backup import CartaPokemonBackupDB
from Models.Model_pydantic.Model_Pokemon_Backup import CartaPokemonBackup

from Operations.Operations_db.db_Operations_Pokemon_Card import (
    crear_carta_pokemon,
    obtener_cartas_pokemon,
    obtener_carta_pokemon_por_nombre,
    modificar_carta_pokemon,
    eliminar_carta_pokemon,
    restaurar_carta_pokemon
)
from Operations.Operations_db.db_Operations_Energie_Card import (
    crear_carta_energia,
    obtener_cartas_energia,
    obtener_carta_energia_por_nombre,
    modificar_carta_energia,
    eliminar_carta_energia,
    restaurar_carta_energia,
    regenerar_csv_energia
)
from Operations.Operations_db.db_Operations_Trainer_Card import (
    crear_carta_entrenador,
    obtener_cartas_entrenador,
    obtener_carta_entrenador_por_nombre,
    modificar_carta_entrenador,
    eliminar_carta_entrenador,
    restaurar_carta_entrenador
)
from db.db_connection import get_session, init_db, async_session
from model_website.home import router as home_router
from db.load_csv_to_supabase import upload_csvs_to_supabase



tags_metadata = [
    {"name": "POKEMON", "description": "Operaciones con cartas Pokémon."},
    {"name": "ENERGIA", "description": "Operaciones con cartas de energía."},
    {"name": "ENTRENADOR", "description": "Operaciones con cartas de entrenador."},
    {"name": "TODAS LAS CARTAS", "description": "Consulta conjunta de todas las cartas disponibles."},
]

# ----------------------------
# CONFIGURACIÓN APP
# ----------------------------
app = FastAPI(openapi_tags=tags_metadata)
app.include_router(home_router)

@app.on_event("startup")
async def startup_event():
    upload_csvs_to_supabase(csv_folder="./csv")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("startup")
async def startup_event():
    async with async_session() as db:
        await regenerar_csv_energia(db)

app.mount("/static", StaticFiles(directory="static"), name="static")
router = APIRouter()
templates = Jinja2Templates(directory="model_website/templates")

# ----------------------------
# WEBSITE
# ----------------------------
@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# ----------------------------
# POKEMON
# ----------------------------
@app.post("/cartas/pokemon/", response_model=CartaPokemon, tags=["POKEMON"])
async def agregar_carta_pokemon(carta: CartaPokemon, db: AsyncSession = Depends(get_session)):
    return await crear_carta_pokemon(db, carta)

@app.get("/cartas/pokemon/", response_model=list[CartaPokemon], tags=["POKEMON"])
async def obtener_cartas_pokemon_endpoint(db: AsyncSession = Depends(get_session)):
    return await obtener_cartas_pokemon(db)

@app.get("/cartas/pokemon/{nombre}", response_model=CartaPokemon, tags=["POKEMON"])
async def obtener_carta_pokemon_por_nombre_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await obtener_carta_pokemon_por_nombre(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return carta

@app.put("/cartas/pokemon/{nombre}", response_model=CartaPokemon, tags=["POKEMON"])
async def modificar_carta_pokemon_endpoint(nombre: str, datos_actualizados: dict, db: AsyncSession = Depends(get_session)):
    carta = await modificar_carta_pokemon(db, nombre, datos_actualizados)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return carta

@app.delete("/cartas/pokemon/{nombre}", response_model=CartaPokemonBackup, tags=["POKEMON"])
async def eliminar_carta_pokemon_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await eliminar_carta_pokemon(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return carta

@app.post("/cartas/pokemon/restaurar/{nombre}", response_model=CartaPokemon, tags=["POKEMON"])
async def restaurar_carta_pokemon_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_pokemon(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada en el respaldo")
    return carta

# ----------------------------
# ENERGIA
# ----------------------------
@app.post("/cartas/energia/", response_model=CartaEnergia, tags=["ENERGIA"])
async def agregar_carta_energia(carta: CartaEnergia, db: AsyncSession = Depends(get_session)):
    return await crear_carta_energia(db, carta)

@app.get("/cartas/energia/", response_model=list[CartaEnergia], tags=["ENERGIA"])
async def obtener_cartas_energia_endpoint(db: AsyncSession = Depends(get_session)):
    return await obtener_cartas_energia(db)

@app.get("/cartas/energia/{nombre}", response_model=CartaEnergia, tags=["ENERGIA"])
async def obtener_carta_energia_por_nombre_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await obtener_carta_energia_por_nombre(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Energia no encontrada")
    return carta

@app.put("/cartas/energia/{nombre}", response_model=CartaEnergia, tags=["ENERGIA"])
async def modificar_carta_energia_endpoint(nombre: str, datos_actualizados: dict, db: AsyncSession = Depends(get_session)):
    carta = await modificar_carta_energia(db, nombre, datos_actualizados)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Energia no encontrada")
    return carta

@app.delete("/cartas/energia/{nombre}", response_model=CartaEnergia, tags=["ENERGIA"])
async def eliminar_carta_energia_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await eliminar_carta_energia(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Energia no encontrada")
    return carta

@app.post("/cartas/energia/restaurar/{nombre}", response_model=CartaEnergia, tags=["ENERGIA"])
async def restaurar_carta_energia_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_energia(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Energia no encontrada en el respaldo")
    return carta

# ----------------------------
# ENTRENADOR
# ----------------------------
@app.post("/cartas/entrenador/", response_model=CartaEntrenador, tags=["ENTRENADOR"])
async def agregar_carta_entrenador(carta: CartaEntrenador, db: AsyncSession = Depends(get_session)):
    return await crear_carta_entrenador(db, carta)

@app.get("/cartas/entrenador/", response_model=list[CartaEntrenador], tags=["ENTRENADOR"])
async def obtener_cartas_entrenador_endpoint(db: AsyncSession = Depends(get_session)):
    return await obtener_cartas_entrenador(db)

@app.get("/cartas/entrenador/{nombre}", response_model=CartaEntrenador, tags=["ENTRENADOR"])
async def obtener_carta_entrenador_por_nombre_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await obtener_carta_entrenador_por_nombre(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return carta

@app.put("/cartas/entrenador/{nombre}", response_model=CartaEntrenador, tags=["ENTRENADOR"])
async def modificar_carta_entrenador_endpoint(nombre: str, datos_actualizados: dict, db: AsyncSession = Depends(get_session)):
    carta = await modificar_carta_entrenador(db, nombre, datos_actualizados)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return carta

@app.delete("/cartas/entrenador/{nombre}", response_model=CartaEntrenador, tags=["ENTRENADOR"])
async def eliminar_carta_entrenador_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await eliminar_carta_entrenador(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return carta

@app.post("/cartas/entrenador/restaurar/{nombre}", response_model=CartaEntrenador, tags=["ENTRENADOR"])
async def restaurar_carta_entrenador_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_entrenador(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada en el respaldo")
    return carta

# ----------------------------
# TODAS LAS CARTAS
# ----------------------------
@app.get("/cartas/", response_model=list[CartModel], tags=["TODAS LAS CARTAS"])
async def obtener_todas_las_cartas(db: AsyncSession = Depends(get_session)):
    cartas_pokemon = await obtener_cartas_pokemon(db)
    cartas_energia = await obtener_cartas_energia(db)
    cartas_entrenador = await obtener_cartas_entrenador(db)
    return cartas_pokemon + cartas_energia + cartas_entrenador
