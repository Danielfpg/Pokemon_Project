from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from Models.Model_db.Model_Pokemon_card_db import CartaPokemonDB
from Models.Model_pydantic.Model_stats import Stats
from Operations.Operations_db.db_Operations_Pokemon_Card import crear_carta_pokemon
from Models.Model_pydantic.Model_Pokemon_card import CartaPokemon
from db.db_connection import get_session

templates = Jinja2Templates(directory="model_website/templates")


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/add_pokemon", response_class=HTMLResponse)
async def mostrar_formulario_pokemon(request: Request):
    return templates.TemplateResponse("add_pokemon.html", {"request": request})

@router.post("/cartas/crear")
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
