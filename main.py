from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from Models.Model_pydantic.Model_Pokemon_card import CartaPokemon
from Models.Model_pydantic.Model_Energie_card import CartaEnergia
from Models.Model_pydantic.Model_Trainer_card import CartaEntrenador
from Models.Model_pydantic.main_model_card import CartModel
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
    restaurar_carta_energia
)
from Operations.Operations_db.db_Operations_Trainer_Card import (
    crear_carta_entrenador,
    obtener_cartas_entrenador,
    obtener_carta_entrenador_por_nombre,
    modificar_carta_entrenador,
    eliminar_carta_entrenador,
    restaurar_carta_entrenador
)
from Operations.Operations_pydantic.Operations_Pokemoncard import *
from db.db_connection import get_session


app = FastAPI()
#--------------------
#POKEMON
#--------------------
@app.post("/cartas/pokemon/", response_model=CartaPokemon)
async def agregar_carta_pokemon(carta: CartaPokemon, db: AsyncSession = Depends(get_session)):
    return await crear_carta_pokemon(db, carta)

@app.get("/cartas/pokemon/", response_model=list[CartaPokemon])
async def obtener_cartas_pokemon_endpoint(db: AsyncSession = Depends(get_session)):
    return await obtener_cartas_pokemon(db)

@app.get("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def obtener_carta_pokemon_por_nombre_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await obtener_carta_pokemon_por_nombre(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return carta

@app.put("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def modificar_carta_pokemon_endpoint(nombre: str, datos_actualizados: dict, db: AsyncSession = Depends(get_session)):
    carta = await modificar_carta_pokemon(db, nombre, datos_actualizados)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return carta

@app.delete("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def eliminar_carta_pokemon_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await eliminar_carta_pokemon(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return carta

@app.post("/cartas/pokemon/restaurar/{nombre}", response_model=CartaPokemon)
async def restaurar_carta_pokemon_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_pokemon(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada en el respaldo")
    return carta
#--------------------
#ENERGIA
#--------------------
@app.post("/cartas/energia/", response_model=CartaEnergia)
async def agregar_carta_energia(carta: CartaEnergia, db: AsyncSession = Depends(get_session)):
    return await crear_carta_energia(db, carta)

@app.get("/cartas/energia/", response_model=list[CartaEnergia])
async def obtener_cartas_energia_endpoint(db: AsyncSession = Depends(get_session)):
    return await obtener_cartas_energia(db)

@app.get("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def obtener_carta_energia_por_nombre_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await obtener_carta_energia_por_nombre(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Energía no encontrada")
    return carta

@app.put("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def modificar_carta_energia_endpoint(nombre: str, datos_actualizados: dict, db: AsyncSession = Depends(get_session)):
    carta = await modificar_carta_energia(db, nombre, datos_actualizados)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Energía no encontrada")
    return carta

@app.delete("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def eliminar_carta_energia_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await eliminar_carta_energia(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Energía no encontrada")
    return carta

@app.post("/cartas/energia/restaurar/{nombre}", response_model=CartaEnergia)
async def restaurar_carta_energia_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_energia(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Energía no encontrada en el respaldo")
    return carta

#--------------------
#ENTRENADOR
#--------------------
@app.post("/cartas/entrenador/", response_model= CartaEntrenador)
async def agregar_carta_entrenador(carta:  CartaEntrenador, db: AsyncSession = Depends(get_session)):
    return await crear_carta_entrenador(db, carta)

@app.get("/cartas/entrenador/", response_model=list[ CartaEntrenador])
async def obtener_cartas_entrenador_endpoint(db: AsyncSession = Depends(get_session)):
    return await obtener_cartas_entrenador(db)

@app.get("/cartas/entrenador/{nombre}", response_model= CartaEntrenador)
async def obtener_carta_entrenador_por_nombre_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await obtener_carta_entrenador_por_nombre(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return carta

@app.put("/cartas/entrenador/{nombre}", response_model= CartaEntrenador)
async def modificar_carta_entrenador_endpoint(nombre: str, datos_actualizados: dict, db: AsyncSession = Depends(get_session)):
    carta = await modificar_carta_entrenador(db, nombre, datos_actualizados)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return carta

@app.delete("/cartas/entrenador/{nombre}", response_model= CartaEntrenador)
async def eliminar_carta_entrenador_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await eliminar_carta_entrenador(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return carta

@app.post("/cartas/entrenador/restaurar/{nombre}", response_model= CartaEntrenador)
async def restaurar_carta_entrenador_endpoint(nombre: str, db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_entrenador(db, nombre)
    if carta is None:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada en el respaldo")
    return carta

#--------------------
#tODAS LAS CARTAS
#--------------------
@app.get("/cartas/", response_model=list[CartModel])
async def obtener_todas_las_cartas(db: AsyncSession = Depends(get_session)):
    cartas_pokemon = await obtener_cartas_pokemon(db)
    cartas_energia = await obtener_cartas_energia(db)
    cartas_entrenador = await obtener_cartas_entrenador(db)
    return cartas_pokemon + cartas_energia + cartas_entrenador
