from typing import List, Optional, Dict, Any
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from Models.Model_Pokemon_card import CartaPokemon
from Operations.Operations_base import write_card_into_csv, leer_todas_las_cartas
import csv

# Leer todas las cartas Pokémon
async def leer_cartas_pokemon_sql(session: AsyncSession) -> List[CartaPokemon]:
    query = select(CartaPokemon)
    result = await session.exec(query)
    return result.all()

# Buscar carta Pokémon por nombre
async def buscar_pokemon_por_nombre_sql(session: AsyncSession, nombre: str) -> Optional[CartaPokemon]:
    query = select(CartaPokemon).where(CartaPokemon.nombre == nombre)
    result = await session.exec(query)
    return result.first()

# Crear carta Pokémon
async def crear_carta_pokemon_sql(session: AsyncSession, carta: CartaPokemon) -> CartaPokemon:
    session.add(carta)
    await session.commit()
    await session.refresh(carta)
    return carta

# Modificar carta Pokémon
async def modificar_carta_pokemon_sql(session: AsyncSession, nombre: str, datos: Dict[str, Any]) -> Optional[CartaPokemon]:
    carta = await buscar_pokemon_por_nombre_sql(session, nombre)
    if carta is None:
        return None

    for key, value in datos.items():
        if key != "id" and hasattr(carta, key) and value is not None:
            setattr(carta, key, value)

    carta.updated_at = datetime.now()
    session.add(carta)
    await session.commit()
    await session.refresh(carta)
    return carta

# Archivo para backup
BACKUP_DATABASE = "Backup.csv"
DATABASE = "Carts.csv"
column_fields = ["id", "nombre", "tipo_carta", "tipo", "stats"]

# Eliminar carta Pokémon (trasladar a backup y eliminar de Carts.csv)
async def eliminar_carta_pokemon_sql(session: AsyncSession, nombre: str) -> Optional[CartaPokemon]:
    # Buscar la carta por nombre
    carta = await buscar_pokemon_por_nombre_sql(session, nombre)
    if carta is None:
        return None

    # Leer todas las cartas actuales (de Carts.csv)
    cartas = leer_todas_las_cartas()

    # Filtrar las cartas que no son la que vamos a eliminar
    nuevas_cartas = [c for c in cartas if not (isinstance(c, CartaPokemon) and c.nombre.lower() == nombre.lower())]

    # Guardar la carta eliminada en Backup.csv
    write_card_into_csv(carta, BACKUP_DATABASE)

    # Reescribir el archivo Carts.csv sin la carta eliminada
    with open(DATABASE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=column_fields)
        writer.writeheader()
        for carta in nuevas_cartas:
            writer.writerow(carta.model_dump())

    return carta
