from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models.Model_db.Model_Pokemon_card_db import CartaPokemonDB
from Models.Model_db.Pokemon_Backup import CartaPokemonBackupDB



async def crear_carta_pokemon(db: AsyncSession, carta: CartaPokemonDB):
    db.add(carta)
    await db.commit()
    await db.refresh(carta)
    return carta


async def obtener_cartas_pokemon(db: AsyncSession):
    result = await db.execute(select(CartaPokemonDB))
    return result.scalars().all()


async def obtener_carta_pokemon_por_nombre(db: AsyncSession, nombre: str):
    result = await db.execute(
        select(CartaPokemonDB).where(CartaPokemonDB.nombre == nombre)
    )
    return result.scalars().first()


async def modificar_carta_pokemon(db: AsyncSession, nombre: str, datos_actualizados: dict):
    carta = await obtener_carta_pokemon_por_nombre(db, nombre)
    if not carta:
        return None

    for key, value in datos_actualizados.items():
        if hasattr(carta, key) and key != "id":
            setattr(carta, key, value)

    await db.commit()
    await db.refresh(carta)
    return carta


async def eliminar_carta_pokemon(db: AsyncSession, nombre: str):
    carta = await obtener_carta_pokemon_por_nombre(db, nombre)
    if not carta:
        return None

    carta_backup = CartaPokemonBackupDB(
        id=carta.id,
        nombre=carta.nombre,
        rare=carta.rare,
        costo_en_bolsa=carta.costo_en_bolsa,
        tipo_carta=carta.tipo_carta,
        tipo=carta.tipo,
        stats_id=carta.stats_id
    )
    db.add(carta_backup)

    await db.delete(carta)
    await db.commit()
    return carta_backup


async def restaurar_carta_pokemon(db: AsyncSession, nombre: str):
    result = await db.execute(
        select(CartaPokemonBackupDB).where(CartaPokemonBackupDB.nombre == nombre)
    )
    backup = result.scalars().first()
    if not backup:
        return None

    carta_restaurada = CartaPokemonDB(
        id=backup.id,
        nombre=backup.nombre,
        rare=backup.rare,
        costo_en_bolsa=backup.costo_en_bolsa,
        tipo_carta=backup.tipo_carta,
        tipo=backup.tipo,
        stats_id=backup.stats_id
    )
    db.add(carta_restaurada)

    await db.delete(backup)
    await db.commit()
    await db.refresh(carta_restaurada)
    return carta_restaurada
