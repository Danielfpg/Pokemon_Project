from fastapi import APIRouter, Request, Form, Depends, Query,HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
#entrenador
from Models.Model_pydantic.Model_Trainer_card import CartaEntrenador
from Models.enums import RarezaEnum
from Operations.Operations_db.db_Operations_Trainer_Card import crear_carta_entrenador,eliminar_carta_entrenador, restaurar_carta_entrenador,modificar_carta_entrenador,obtener_carta_entrenador_por_nombre
from Models.Model_db.Model_Trainer_card_db import CartaEntrenadorDB
from Models.Model_db.Trainer_Backup import CartaEntrenadorBackupDB
#pokemon
from Models.Model_db.Model_Pokemon_card_db import CartaPokemonDB
from Models.Model_pydantic.Model_stats import Stats
from Operations.Operations_db.db_Operations_Pokemon_Card import crear_carta_pokemon,eliminar_carta_pokemon,modificar_carta_pokemon,restaurar_carta_pokemon,obtener_carta_pokemon_por_nombre
from Models.Model_pydantic.Model_Pokemon_card import CartaPokemon
from Models.enums import RarezaEnum
#energia
from Models.Model_db.Model_Energie_card_db import CartaEnergiaDB
from Operations.Operations_db.db_Operations_Energie_Card import crear_carta_energia, eliminar_carta_energia, \
    restaurar_carta_energia, modificar_carta_energia, obtener_carta_energia_por_nombre
from Models.Model_pydantic.Model_Energie_card import CartaEnergia
from db.db_connection import get_session
from Models.Model_db.Energie_Backup import CartaEnergiaBackupDB
import csv
import os
templates = Jinja2Templates(directory="model_website/templates")


router = APIRouter()


@router.get("/", response_class=HTMLResponse, tags=["Home"])
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
#--------------------
#POKEMON
#--------------------
@router.get("/add_pokemon", response_class=HTMLResponse, tags=["Pokémon"])
async def mostrar_formulario_pokemon(request: Request):
    return templates.TemplateResponse("add_pokemon.html", {"request": request})

@router.post("/cartas/crear/pokemon", tags=["Pokémon"])
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


@router.get("/cartas/editar/pokemon/{nombre}")
async def formulario_editar_pokemon(nombre: str, request: Request, db: AsyncSession = Depends(get_session)):
    carta = await obtener_carta_pokemon_por_nombre(db, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada")

    tipos_disponibles = [
        "Normal", "Fuego", "Agua", "Eléctrico", "Planta", "Hielo", "Lucha", "Veneno",
        "Tierra", "Volador", "Psíquico", "Bicho", "Roca", "Fantasma", "Dragón", "Siniestro", "Acero", "Hada"
    ]

    tipo_split = [t.strip() for t in carta.tipo.split(',')]
    tipo1 = tipo_split[0] if len(tipo_split) > 0 else ""
    tipo2 = tipo_split[1] if len(tipo_split) > 1 else ""

    rareza_categorizada = {
        "Rarezas básicas": [
            "común", "poco_común", "rara", "rara_holográfica",
            "doble_rara", "rara_de_ilustración", "rara_de_ilustración_especial", "rara_brillante"
        ],
        "Rarezas especiales (modernas)": [
            "rara_de_personaje", "super_rara_de_personaje", "rara_de_arte", "rara_de_arte_especial",
            "súper_rara_brillante", "ultra_rara", "híper_rara", "rara_secreta", "promocional"
        ],
        "Rarezas históricas / específicas de sets": [
            "rara_radiant", "rara_asombrosa", "legendaria", "rara_prime", "especie_delta", "ace_spec"
        ],
        "No son rarezas, pero se suelen tratar como tales": [
            "ex", "gx", "v", "vmax", "vstar", "tag team"
        ]
    }

    return templates.TemplateResponse("mod_pokemon.html", {
        "request": request,
        "carta": carta,
        "tipo1": tipo1,
        "tipo2": tipo2,
        "tipos": tipos_disponibles,
        "rareza_categorizada": rareza_categorizada
    })

@router.post("/cartas/editar/pokemon/{nombre}")
async def editar_pokemon(
    nombre: str,
    request: Request,
    rare: str = Form(...),
    costo_en_bolsa: float = Form(...),
    tipo_carta: str = Form(...),
    tipo: str = Form(...),
    stats_hp: int = Form(..., alias="hp"),
    stats_attack: int = Form(..., alias="attack"),
    stats_defense: int = Form(..., alias="defense"),
    stats_speed: int = Form(..., alias="speed"),
    stats_special_atk: int = Form(..., alias="special_atk"),
    stats_special_def: int = Form(..., alias="special_def"),
    db: AsyncSession = Depends(get_session)
):
    carta = await obtener_carta_pokemon_por_nombre(db, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada")

    datos_actualizados = {
        "rare": rare,
        "costo_en_bolsa": costo_en_bolsa,
        "tipo_carta": tipo_carta,
        "tipo": tipo,
    }

    # Actualizar carta
    for key, value in datos_actualizados.items():
        setattr(carta, key, value)

    # Actualizar stats
    if carta.stats:
        carta.stats.hp = stats_hp
        carta.stats.attack = stats_attack
        carta.stats.defense = stats_defense
        carta.stats.speed = stats_speed
        carta.stats.special_atk = stats_special_atk
        carta.stats.special_def = stats_special_def

    await db.commit()
    await db.refresh(carta)

    return RedirectResponse(url="/", status_code=303)

@router.get("/ver_pokemones", response_class=HTMLResponse, tags=["Pokémon"])
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
@router.get("/add_entrenador", response_class=HTMLResponse, tags=["Entrenador"])
async def mostrar_formulario_entrenador(request: Request):
    return templates.TemplateResponse("add_entrenador.html", {"request": request})

@router.post("/cartas/crear/entrenador", tags=["Entrenador"])
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

@router.get("/ver_entrenador", response_class=HTMLResponse, tags=["Entrenador"])
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
@router.post("/cartas/editar/entrenador/{nombre}")
async def actualizar_carta_entrenador(
    nombre: str,
    id: int = Form(...),
    rare: str = Form(...),
    costo_en_bolsa: float = Form(...),
    subtipo: str = Form(...),
    efecto: str = Form(...),
    tiempo: str = Form(...),
    db: AsyncSession = Depends(get_session)
):
    nombre = nombre.strip()
    print("Nombre recibido en POST:", nombre)
    carta_existente = await obtener_carta_entrenador_por_nombre(db, nombre)
    if not carta_existente:
        raise HTTPException(status_code=404, detail="Carta no encontrada")

    datos_actualizados = {
        "id": id,
        "rare": rare,
        "costo_en_bolsa": costo_en_bolsa,
        "subtipo": subtipo,
        "efecto": efecto,
        "tiempo": tiempo
    }

    carta_actualizada = await modificar_carta_entrenador(db, nombre, datos_actualizados)

    # Actualizar el CSV
    archivo = "Entrenador.csv"
    if os.path.exists(archivo):
        with open(archivo, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))

        # Modificar la fila correspondiente
        for fila in filas:
            if fila["nombre"] == nombre:
                fila.update({k: str(v) for k, v in datos_actualizados.items()})
                fila["nombre"] = nombre
                fila["tipo_carta"] = "entrenador"

        # Campos válidos para guardar en el CSV
        campos_validos = ["id", "nombre", "rare", "costo_en_bolsa", "tipo_carta", "subtipo", "efecto", "tiempo"]

        # Limpiar filas antes de escribirlas
        filas_limpias = []
        for fila in filas:
            fila_limpia = {campo: fila.get(campo, "") for campo in campos_validos}
            filas_limpias.append(fila_limpia)

        # Escribir de nuevo el archivo limpio
        with open(archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos_validos)
            writer.writeheader()
            writer.writerows(filas_limpias)

    return RedirectResponse(url="/ver_entrenador", status_code=303)
@router.get("/cartas/editar/entrenador/{nombre}", response_class=HTMLResponse, tags=["Entrenador"])
async def formulario_editar_entrenador(nombre: str, request: Request, db: AsyncSession = Depends(get_session)):
    nombre = nombre.strip()
    carta = await obtener_carta_entrenador_por_nombre(db, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada")

    return templates.TemplateResponse("mod_entrenador.html", {
        "request": request,
        "carta": carta,
        "rarezas": RarezaEnum
    })
@router.post("/cartas/eliminar/entrenador", response_class=HTMLResponse, tags=["Entrenador"])
async def eliminar_entrenador(nombre: str = Form(...), db: AsyncSession = Depends(get_session)):
    backup = await eliminar_carta_entrenador(db, nombre)
    if not backup:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return RedirectResponse("/ver_entrenador", status_code=303)

@router.post("/cartas/restaurar/entrenador", response_class=HTMLResponse, tags=["Entrenador"])
async def restaurar_entrenador(nombre: str = Form(...), db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_entrenador(db, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada en respaldo")
    return RedirectResponse("/ver_entrenador", status_code=303)
@router.get("/recuperar_entrenador", response_class=HTMLResponse, tags=["Entrenador"])
async def ver_entrenador_respaldo(
    request: Request,
    session: AsyncSession = Depends(get_session),
    q: str = Query(default=None)
):
    stmt = select(CartaEntrenadorBackupDB)  # Asegúrate de tener este modelo

    if q:
        stmt = stmt.where(CartaEntrenadorBackupDB.nombre.ilike(f"%{q}%"))

    result = await session.execute(stmt)
    entrenador = result.scalars().all()

    return templates.TemplateResponse("recuperar_entrenador.html", {
        "request": request,
        "entrenadores": entrenador
    })

# --------------------
# ENERGIA
# --------------------

@router.get("/add_energia", response_class=HTMLResponse, tags=["Energía"])
async def mostrar_formulario_energia(request: Request):
    return templates.TemplateResponse("add_energia.html", {"request": request})

@router.post("/cartas/crear/energia", tags=["Energía"])
async def agregar_carta_energia_form(
    nombre: str = Form(...),
    id: int = Form(...),
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

@router.get("/ver_energia", response_class=HTMLResponse, tags=["Energía"])
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
@router.post("/cartas/editar/energia/{nombre}")
async def actualizar_carta_energia(
    nombre: str,
    id: int = Form(...),
    tipo: str = Form(...),
    especial: bool = Form(False),
    rare: str = Form(...),
    costo_en_bolsa: float = Form(...),
    db: AsyncSession = Depends(get_session)
):
    nombre = nombre.strip()
    print("Nombre recibido en POST:", nombre)
    carta_existente = await obtener_carta_energia_por_nombre(db, nombre)
    if not carta_existente:
        raise HTTPException(status_code=404, detail="Carta no encontrada")

    datos_actualizados = {
        "id": id,
        "rare": rare,
        "costo_en_bolsa": costo_en_bolsa,
        "tipo": tipo,
        "especial": especial,

    }

    carta_actualizada = await modificar_carta_energia(db, nombre, datos_actualizados)

    # Actualizar el CSV
    archivo = "Energia.csv"
    if os.path.exists(archivo):
        with open(archivo, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))

        # Modificar la fila correspondiente
        for fila in filas:
            if fila["nombre"] == nombre:
                fila.update({k: str(v) for k, v in datos_actualizados.items()})
                fila["nombre"] = nombre
                fila["tipo_carta"] = "energia"

        # Campos válidos para guardar en el CSV
        campos_validos = ["id", "nombre", "rare", "costo_en_bolsa", "tipo","especial"]

        # Limpiar filas antes de escribirlas
        filas_limpias = []
        for fila in filas:
            fila_limpia = {campo: fila.get(campo, "") for campo in campos_validos}
            filas_limpias.append(fila_limpia)

        # Escribir de nuevo el archivo limpio
        with open(archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos_validos)
            writer.writeheader()
            writer.writerows(filas_limpias)

    return RedirectResponse(url="/ver_energia", status_code=303)
@router.get("/cartas/editar/energia/{nombre}", response_class=HTMLResponse, tags=["energia"])
async def formulario_editar_energia(nombre: str, request: Request, db: AsyncSession = Depends(get_session)):
    nombre = nombre.strip()
    carta = await obtener_carta_energia_por_nombre(db, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada")

    return templates.TemplateResponse("mod_energia.html", {
        "request": request,
        "carta": carta,
        "rarezas": RarezaEnum
    })
@router.post("/cartas/eliminar/energia", response_class=HTMLResponse, tags=["Energía"])
async def eliminar_energia(nombre: str = Form(...), db: AsyncSession = Depends(get_session)):
    backup = await eliminar_carta_energia(db, nombre)
    if not backup:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return RedirectResponse("/ver_energia", status_code=303)

@router.post("/cartas/restaurar/energia", response_class=HTMLResponse, tags=["Energía"])
async def restaurar_energia(nombre: str = Form(...), db: AsyncSession = Depends(get_session)):
    carta = await restaurar_carta_energia(db, nombre)
    if not carta:
        raise HTTPException(status_code=404, detail="Carta no encontrada en respaldo")
    return RedirectResponse("/ver_energia", status_code=303)
@router.get("/recuperar_energia", response_class=HTMLResponse, tags=["Energía"])
async def recuperar_energia(
    request: Request,
    session: AsyncSession = Depends(get_session),
    q: str = Query(default=None)
):
    stmt = select(CartaEnergiaBackupDB)  # tu modelo de respaldo

    if q:
        stmt = stmt.where(CartaEnergiaBackupDB.nombre.ilike(f"%{q}%"))

    result = await session.execute(stmt)
    energias = result.scalars().all()

    return templates.TemplateResponse("recuperar_energia.html", {
        "request": request,
        "energias": energias
    })