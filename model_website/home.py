from fastapi import APIRouter, Request, Form, Depends, Query,HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from Models.Model_pydantic.Model_Trainer_card import CartaEntrenador
from Operations.Operations_db.db_Operations_Trainer_Card import crear_carta_entrenador,eliminar_carta_entrenador, restaurar_carta_entrenador
from Models.Model_db.Model_Trainer_card_db import CartaEntrenadorDB

from Models.Model_db.Model_Pokemon_card_db import CartaPokemonDB
from Models.Model_pydantic.Model_stats import Stats
from Operations.Operations_db.db_Operations_Pokemon_Card import crear_carta_pokemon
from Models.Model_pydantic.Model_Pokemon_card import CartaPokemon
from db.db_connection import get_session

from Models.Model_db.Model_Energie_card_db import CartaEnergiaDB
from Operations.Operations_db.db_Operations_Energie_Card import crear_carta_energia,eliminar_carta_energia,restaurar_carta_energia
from Models.Model_pydantic.Model_Energie_card import CartaEnergia
from db.db_connection import get_session



templates = Jinja2Templates(directory="model_website/templates")


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
#--------------------
#POKEMON
#--------------------
@router.get("/add_pokemon", response_class=HTMLResponse)
async def mostrar_formulario_pokemon(request: Request):
    return templates.TemplateResponse("add_pokemon.html", {"request": request})

@router.post("/cartas/crear/pokemon")
async def agregar_carta_pokemon_form(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    tipo_carta: str = Form(...),
    tipo: str = Form(...),
    rare: str = Form(...),
    costo_en_bolsa: float = Form(...),
    hp: int = Form(...),
    attack: int = Form(...),
    defense: int = Form(...),
    speed: int = Form(...),
    special_atk: int = Form(...),
    special_def: int = Form(...),
    db: AsyncSession = Depends(get_session)
):
    if not tipo or tipo.strip() == "":
        return templates.TemplateResponse("add_pokemon.html", {
            "request": request,
            "error": "Debe seleccionar al menos un tipo Pokémon."
        })

    stats = Stats(
        hp=hp,
        attack=attack,
        defense=defense,
        speed=speed,
        special_atk=special_atk,
        special_def=special_def
    )

    carta = CartaPokemon(
        id=id,
        nombre=nombre,
        tipo_carta=tipo_carta.lower(),
        tipo=tipo,
        rare=rare,
        costo_en_bolsa=costo_en_bolsa,
        stats=stats
    )

    await crear_carta_pokemon(db, carta)

    return RedirectResponse(url="/", status_code=303)
@router.get("/ver_pokemones", response_class=HTMLResponse)
async def ver_pokemones(
    request: Request,
    session: AsyncSession = Depends(get_session),
    q: str = Query(default=None)
):
    stmt = select(CartaPokemonDB).options(selectinload(CartaPokemonDB.stats))

    if q:
        stmt = stmt.where(CartaPokemonDB.nombre.ilike(f"%{q}%"))

    result = await session.execute(stmt)
    pokemones = result.scalars().all()

    return templates.TemplateResponse("ver_pokemones.html", {
        "request": request,
        "pokemones": pokemones
    })
#--------------------
#ENTRENADOR
#--------------------
@router.get("/add_entrenador", response_class=HTMLResponse)
async def mostrar_formulario_entrenador(request: Request):
    return templates.TemplateResponse("add_entrenador.html", {"request": request})

@router.post("/cartas/crear/entrenador")
async def agregar_carta_entrenador_form(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    tipo_carta: str = Form(...),
    subtipo: str = Form(...),
    efecto: str = Form(...),
    tiempo: str = Form(...),
    rare: str = Form(...),
    costo_en_bolsa: float = Form(...),
    db: AsyncSession = Depends(get_session)
):
    carta = CartaEntrenador(
        id=id,
        nombre=nombre,
        tipo_carta=tipo_carta.lower(),
        subtipo=subtipo,
        efecto=efecto,
        tiempo=tiempo,
        rare=rare,
        costo_en_bolsa=costo_en_bolsa
    )

    await crear_carta_entrenador(db, carta)

    return RedirectResponse(url="/", status_code=303)

@router.get("/ver_entrenador", response_class=HTMLResponse)
async def ver_entrenador(
    request: Request,
    session: AsyncSession = Depends(get_session),
    q: str = Query(default=None)
):
    stmt = select(CartaEntrenadorDB)

    if q:
        stmt = stmt.where(CartaEntrenadorDB.nombre.ilike(f"%{q}%"))

    result = await session.execute(stmt)
    entrenador = result.scalars().all()

    return templates.TemplateResponse("ver_entrenador.html", {
        "request": request,
        "entrenadores": entrenador
    })

@router.post("/cartas/eliminar/entrenador", response_class=HTMLResponse)
async def eliminar_entrenador(nombre: str = Form(...), db: AsyncSession = Depends(get_session)):
    backup = await eliminar_carta_entrenador(db, nombre)
    if not backup:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return RedirectResponse("/ver_entrenador", status_code=303)

@router.post("/cartas/restaurar/entrenador", response_class=HTMLResponse)
async def restaurar_entrenador(nombre: str = Form(...), db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_entrenador(db, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada en respaldo")
    return RedirectResponse("/ver_entrenador", status_code=303)

# --------------------
# ENERGIA
# --------------------

@router.get("/add_energia", response_class=HTMLResponse)
async def mostrar_formulario_energia(request: Request):
    return templates.TemplateResponse("add_energia.html", {"request": request})

@router.post("/cartas/crear/energia")
async def agregar_carta_energia_form(
    request: Request,
    id: int = Form(...),
    nombre: str = Form(...),
    tipo_carta: str = Form(...),
    tipo: str = Form(...),
    especial: bool = Form(False),
    rare: str = Form(...),
    costo_en_bolsa: float = Form(...),
    db: AsyncSession = Depends(get_session)
):
    carta = CartaEnergia(
        id=id,
        nombre=nombre,
        tipo_carta=tipo_carta.lower(),
        tipo=tipo,
        especial=especial,
        rare=rare,
        costo_en_bolsa=costo_en_bolsa
    )

    await crear_carta_energia(db, carta)

    return RedirectResponse(url="/", status_code=303)

@router.get("/ver_energia", response_class=HTMLResponse)
async def ver_energia(
    request: Request,
    session: AsyncSession = Depends(get_session),
    q: str = Query(default=None)
):
    stmt = select(CartaEnergiaDB)

    if q:
        stmt = stmt.where(CartaEnergiaDB.nombre.ilike(f"%{q}%"))

    result = await session.execute(stmt)
    energia = result.scalars().all()

    return templates.TemplateResponse("ver_energia.html", {
        "request": request,
        "energias": energia
    })

@router.post("/cartas/eliminar/energia", response_class=HTMLResponse)
async def eliminar_energia(nombre: str = Form(...), db: AsyncSession = Depends(get_session)):
    backup = await eliminar_carta_energia(db, nombre)
    if not backup:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return RedirectResponse("/ver_energia", status_code=303)

@router.post("/cartas/restaurar/energia", response_class=HTMLResponse)
async def restaurar_energia(nombre: str = Form(...), db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_energia(db, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada en respaldo")
    return RedirectResponse("/ver_energia", status_code=303)