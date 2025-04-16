from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from typing import List

from Operations.Operations_base import (
    leer_todas_las_cartas,
    buscar_carta_por_nombre,
    modificar_carta,
    eliminar_carta,
    filtrar_cartas_por_tipo,
    agregar_carta,
    restaurar_carta
)

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
from Operations.Operations_Energiecard import (
    leer_cartas_energia,
    buscar_energia_por_nombre,
    crear_carta_energia,
    modificar_carta_energia,
    eliminar_carta_energia
)
from Models.Model_Energie_card import CartaEnergia
from Models.Model_Trainer_card import CartaEntrenador
from Models.main_model_card import CartModel
from Models.Model_Pokemon_card import CartaPokemon

app = FastAPI()

# ----------------------------------------
#         Endpoints Generales
# ----------------------------------------

@app.get("/cartas", response_model=List[CartModel])
async def todas_las_cartas():
    return leer_todas_las_cartas()

@app.get("/cartas/{nombre}", response_model=CartModel)
async def obtener_carta(nombre: str):
    carta = buscar_carta_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return carta

@app.get("/cartas/tipo/{tipo}", response_model=List[CartModel])
async def cartas_por_tipo(tipo: str):
    filtradas = filtrar_cartas_por_tipo(tipo)
    if not filtradas:
        raise HTTPException(status_code=404, detail="No se encontraron cartas del tipo especificado")
    return filtradas

@app.post("/cartas/restaurar/{nombre}", response_model=CartModel)
async def restaurar(nombre: str):
    carta = restaurar_carta(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="No se encontró la carta en el backup")
    return carta

# ----------------------------------------
#       Endpoints Específicos Pokémon
# ----------------------------------------

@app.get("/cartas/pokemon", response_model=List[CartaPokemon])
async def obtener_cartas_pokemon():
    return leer_cartas_pokemon()

@app.get("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def obtener_pokemon_por_nombre(nombre: str):
    carta = buscar_pokemon_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return carta

@app.post("/cartas/pokemon", response_model=CartaPokemon)
async def nueva_carta_pokemon(carta: CartaPokemon):
    return crear_carta_pokemon(carta)

@app.put("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def editar_carta_pokemon(nombre: str, data: dict):
    modificada = modificar_carta_pokemon(nombre, data)
    if not modificada:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return modificada

@app.delete("/cartas/pokemon/{nombre}", response_model=CartaPokemon)
async def borrar_carta_pokemon(nombre: str):
    eliminada = eliminar_carta_pokemon(nombre)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Carta Pokémon no encontrada")
    return eliminada
# ----------------------------------------
#       Endpoints Específicos Entrenador
# ----------------------------------------
@app.get("/cartas/entrenador", response_model=List[CartaEntrenador])
async def obtener_carta_entrenador():
    return leer_todas_las_cartas()

@app.get("/cartas/entrenador/{nombre}", response_model=CartaEntrenador)
async def obtener_carta_entrenador(nombre: str):
    carta = buscar_entrenador_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return carta

@app.post("/cartas/entrenador", response_model=CartaEntrenador)
async def nueva_carta_entrenador(carta: CartaEntrenador):
    return crear_carta_entrenador(carta)

@app.put("/cartas/Entrenador/{nombre}", response_model=CartaEntrenador)
async def editar_carta_entrenador(nombre: str, data: dict):
    modificada = modificar_carta_entrenador(nombre, data)
    if not modificada:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return modificada

@app.delete("/cartas/Entrenador/{nombre}", response_model=CartaEntrenador)
async def borrar_carta_entrenador(nombre: str):
    eliminada = eliminar_carta_entrenador(nombre)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Carta Entrenador no encontrada")
    return eliminada

# ----------------------------------------
#       Endpoints Específicos Energia
# ----------------------------------------

@app.get("/cartas/Energia", response_model=List[CartaEnergia])
async def obtener_carta_energia():
    return leer_todas_las_cartas()

@app.get("/cartas/Energia/{nombre}", response_model=CartaEnergia)
async def obtener_carta_energia(nombre: str):
    carta = buscar_energia_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Energia no encontrada")
    return carta

@app.post("/cartas/Energia", response_model=CartaEnergia)
async def nueva_carta_energia(carta: CartaEnergia):
    return crear_carta_energia(carta)

@app.put("/cartas/Energia/{nombre}/", response_model=CartaEnergia)
async def editar_carta_energia(nombre: str, data: dict):
    modificada = modificar_carta_energia(nombre, data)
    if not modificada:
        raise HTTPException(status_code=404, detail="Energia no encontrada")
    return modificada

@app.delete("/carta/Energia/{nombre}", response_model=CartaEnergia)
async def borrar_carta_energia(nombre: str):
    eliminada = eliminar_carta_energia(nombre)
    if not eliminada:
        return HTTPException(status_code=404, detail="Energia no encontrada")
    return eliminada

# ----------------------------------------
#           Manejo de Errores
# ----------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "ERROR",
            "detail": exc.detail,
            "path": request.url.path
        },
    )

@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)
