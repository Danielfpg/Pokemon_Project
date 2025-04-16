from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from Operations.Operations_base import*
from typing import List

app = FastAPI()

#----------------------------------------
#           Endpoints mapp
#----------------------------------------

# Mostrar todas las cartas
@app.get("/cartas", response_model=List[CartModel])
async def todas_las_cartas():
    return leer_todas_las_cartas()

# Buscar carta por nombre (cualquier tipo)
@app.get("/cartas/{nombre}", response_model=CartModel)
async def obtener_carta(nombre: str):
    carta = buscar_carta_por_nombre(nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return carta

# Crear nueva carta (puede ser de cualquier tipo)
@app.post("/cartas", response_model=CartModel)
async def crear_carta(carta: CartModel):
    return agregar_carta(carta)

# Modificar carta por nombre (no modifica ID)
@app.put("/cartas/{nombre}", response_model=CartModel)
async def actualizar_carta(nombre: str, data: dict):
    modificada = modificar_carta(nombre, data)
    if not modificada:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return modificada

# Eliminar carta por nombre
@app.delete("/cartas/{nombre}", response_model=CartModel)
async def eliminar_carta_endpoint(nombre: str):
    eliminada = eliminar_carta(nombre)  # sin await
    if not eliminada:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return eliminada




# Filtrar por tipo de carta
@app.get("/cartas/tipo/{tipo}", response_model=List[CartModel])
async def cartas_por_tipo(tipo: str):
    filtradas = filtrar_cartas_por_tipo(tipo)
    if not filtradas:
        raise HTTPException(status_code=404, detail="No se encontraron cartas del tipo especificado")
    return filtradas

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "ERROR 404",
            "detail": exc.detail,
            "path": request.url.path
        },
    )

@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)