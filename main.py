from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from typing import List

# Operaciones base
from Operations.Operations_base import (
    leer_todas_las_cartas,
    buscar_carta_por_nombre,
    filtrar_cartas_por_tipo,
    restaurar_carta
)

# Operaciones específicas
from Operations.Operations_Pokemoncard import (
    leer_cartas_pokemon,
    buscar_pokemon_por_nombre,
    crear_carta_pokemon,
    modificar_carta_pokemon,
    eliminar_carta_pokemon
)
from Operations.Operations_Trainercard import (
    leer_cartas_entrenador,
    buscar_entrenador_por_nombre,
    crear_carta_entrenador,
    modificar_carta_entrenador,
    eliminar_carta_entrenador
)
from db.db_Operations_Energie_Card import (
    leer_cartas_energia_sql,
    buscar_energia_por_nombre_sql,
    crear_carta_energia_sql,
    modificar_carta_energia_sql,
    eliminar_carta_energia_sql
)
from Operations.Operations_Energiecard import (
    leer_cartas_energia,
    buscar_energia_por_nombre,
    crear_carta_energia,
    modificar_carta_energia,
    eliminar_carta_energia
)

# Modelos
from Models.Model_Pokemon_card import CartaPokemon
from Models.Model_Trainer_card import CartaEntrenador
from Models.Model_Energie_card import CartaEnergia
from Models.main_model_card import CartModel
from db.db_connection import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
app = FastAPI(title="Pokémon Card Manager API")

# ----------------------------------------
#         Endpoints Generales
# ----------------------------------------

@app.get("/cartas", response_model=List[CartModel])
async def obtener_todas_las_cartas():
    return leer_todas_las_cartas()

@app.get("/cartas/{nombre}", response_model=CartModel)
async def obtener_carta_por_nombre(nombre: str):
    carta = buscar_carta_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se encontró ninguna carta con el nombre '{nombre}'.")
    return carta

@app.get("/cartas/tipo/{tipo}", response_model=List[CartModel])
async def obtener_cartas_por_tipo(tipo: str):
    cartas = filtrar_cartas_por_tipo(tipo)
    if not cartas:
        raise HTTPException(status_code=404, detail=f"No hay cartas registradas del tipo '{tipo}'.")
    return cartas

@app.post("/cartas/restaurar/{nombre}", response_model=CartModel)
async def restaurar_desde_backup(nombre: str):
    carta = restaurar_carta(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se encontró una copia de seguridad de la carta '{nombre}'.")
    return carta

# ----------------------------------------
#         Endpoints Pokémon
# ----------------------------------------

@app.get("/cartas/pokemon", response_model=List[CartaPokemon])
async def obtener_todas_pokemon():
    return leer_cartas_pokemon()

@app.get("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def obtener_pokemon(nombre: str):
    carta = buscar_pokemon_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"Carta Pokémon '{nombre}' no encontrada.")
    return carta

@app.post("/cartas/pokemon", response_model=CartaPokemon)
async def crear_pokemon(carta: CartaPokemon):
    return crear_carta_pokemon(carta)

@app.put("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def editar_pokemon(nombre: str, data: dict):
    carta = modificar_carta_pokemon(nombre, data)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se pudo modificar. La carta Pokémon '{nombre}' no existe.")
    return carta

@app.delete("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def eliminar_pokemon(nombre: str):
    carta = eliminar_carta_pokemon(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se pudo eliminar. La carta Pokémon '{nombre}' no existe.")
    return carta

# ----------------------------------------
#         Endpoints Entrenador
# ----------------------------------------

@app.get("/cartas/entrenador", response_model=List[CartaEntrenador])
async def obtener_todas_entrenador():
    return leer_cartas_entrenador()

@app.get("/cartas/entrenador/{nombre}", response_model=CartaEntrenador)
async def obtener_entrenador(nombre: str):
    carta = buscar_entrenador_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"Carta Entrenador '{nombre}' no encontrada.")
    return carta

@app.post("/cartas/entrenador", response_model=CartaEntrenador)
async def crear_entrenador(carta: CartaEntrenador):
    return crear_carta_entrenador(carta)

@app.put("/cartas/entrenador/{nombre}", response_model=CartaEntrenador)
async def editar_entrenador(nombre: str, data: dict):
    carta = modificar_carta_entrenador(nombre, data)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se pudo modificar. La carta Entrenador '{nombre}' no existe.")
    return carta

@app.delete("/cartas/entrenador/{nombre}", response_model=CartaEntrenador)
async def eliminar_entrenador(nombre: str):
    carta = eliminar_carta_entrenador(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se pudo eliminar. La carta Entrenador '{nombre}' no existe.")
    return carta

# ----------------------------------------
#         Endpoints Energía
# ----------------------------------------

@app.get("/cartas/energia", response_model=List[CartaEnergia])
async def obtener_todas_energia():
    return leer_cartas_energia()

@app.get("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def obtener_energia(nombre: str):
    carta = buscar_energia_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"Carta Energía '{nombre}' no encontrada.")
    return carta

@app.post("/cartas/energia", response_model=CartaEnergia)
async def crear_energia(carta: CartaEnergia):
    return crear_carta_energia(carta)

@app.put("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def editar_energia(nombre: str, data: dict):
    carta = modificar_carta_energia(nombre, data)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se pudo modificar. La carta Energía '{nombre}' no existe.")
    return carta

@app.delete("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def eliminar_energia(nombre: str):
    carta = eliminar_carta_energia(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se pudo eliminar. La carta Energía '{nombre}' no existe.")
    return carta
""""    
# ----------------------------------------
#         Endpoints Energía (Base de datos)
# ----------------------------------------
@app.get("/cartas/energia", response_model=List[CartaEnergia])
async def obtener_todas_energia(session: AsyncSession = Depends(get_db_session)):
    return await leer_cartas_energia_sql(session)

@app.get("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def obtener_energia(nombre: str, session: AsyncSession = Depends(get_db_session)):
    carta = await buscar_energia_por_nombre_sql(session, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"Carta Energía '{nombre}' no encontrada.")
    return carta

@app.post("/cartas/energia", response_model=CartaEnergia)
async def crear_energia(carta: CartaEnergia, session: AsyncSession = Depends(get_db_session)):
    return await crear_carta_energia_sql(session, carta)

@app.put("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def editar_energia(nombre: str, data: dict, session: AsyncSession = Depends(get_db_session)):
    carta = await modificar_carta_energia_sql(session, nombre, data)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se pudo modificar. La carta Energía '{nombre}' no existe.")
    return carta

@app.delete("/cartas/energia/{nombre}", response_model=CartaEnergia)
async def eliminar_energia(nombre: str, session: AsyncSession = Depends(get_db_session)):
    carta = await eliminar_carta_energia_sql(session, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail=f"No se pudo eliminar. La carta Energía '{nombre}' no existe.")
    return carta
"""
# ----------------------------------------
#        Manejo general de errores
# ----------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "mensaje": "Ocurrió un error procesando tu solicitud.",
            "detalle": exc.detail,
            "ruta": str(request.url)
        },
    )

@app.get("/error")
async def probar_error():
    raise HTTPException(status_code=400, detail="Esto es solo una prueba de error.")
