from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models.Model_db.Model_Pokemon_card_db import CartaPokemonDB
from Models.Model_db.Pokemon_Backup import CartaPokemonBackupDB
from sqlalchemy.exc import SQLAlchemyError

# Crear una nueva carta Pokémon
async def crear_carta_pokemon(db: AsyncSession, carta: CartaPokemonDB):
    try:
        db.add(carta)
        await db.commit()
        await db.refresh(carta)
        return carta
    except SQLAlchemyError as e:
        await db.rollback()
        raise Exception(f"Error al crear carta Pokémon: {str(e)}")

# Obtener todas las cartas Pokémon
async def obtener_cartas_pokemon(db: AsyncSession):
    try:
        result = await db.execute(select(CartaPokemonDB))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener cartas Pokémon: {str(e)}")

# Obtener una carta Pokémon por nombre
async def obtener_carta_pokemon_por_nombre(db: AsyncSession, nombre: str):
    try:
        result = await db.execute(
            select(CartaPokemonDB).where(CartaPokemonDB.nombre == nombre)
        )
        return result.scalars().first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener carta Pokémon por nombre: {str(e)}")

# Modificar una carta Pokémon
async def modificar_carta_pokemon(db: AsyncSession, nombre: str, datos_actualizados: dict):
    try:
        carta = await obtener_carta_pokemon_por_nombre(db, nombre)
        if not carta:
            return None

        for key, value in datos_actualizados.items():
            if hasattr(carta, key) and key != "id":
                setattr(carta, key, value)

        await db.commit()
        await db.refresh(carta)
        return carta
    except SQLAlchemyError as e:
        await db.rollback()
        raise Exception(f"Error al modificar carta Pokémon: {str(e)}")

# Eliminar una carta Pokémon
async def eliminar_carta_pokemon(db: AsyncSession, nombre: str):
    try:
        carta = await obtener_carta_pokemon_por_nombre(db, nombre)
        if not carta:
            return None

        # Hacer un backup de la carta antes de eliminarla
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
    except SQLAlchemyError as e:
        await db.rollback()
        raise Exception(f"Error al eliminar carta Pokémon: {str(e)}")

# Restaurar una carta Pokémon desde un backup
async def restaurar_carta_pokemon(db: AsyncSession, nombre: str):
    try:
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
    except SQLAlchemyError as e:
        await db.rollback()
        raise Exception(f"Error al restaurar carta Pokémon: {str(e)}")
