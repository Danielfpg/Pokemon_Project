from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models.Model_db.Model_Pokemon_card_db import CartaPokemonDB
from Models.Model_db.Pokemon_Backup import CartaPokemonBackupDB
from sqlalchemy.exc import SQLAlchemyError
from Models.Model_pydantic.Model_Pokemon_card import CartaPokemon
from Models.Model_db.Model_stats_db import StatsDB
# Crear una nueva carta Pokémon
async def crear_carta_pokemon(db: AsyncSession, carta: CartaPokemon):
    try:
        carta_data = carta.dict(exclude={"stats"})
        stats_data = carta.stats.dict()

        # Validar campo tipo
        tipo = carta_data.get("tipo")
        if not tipo:
            raise ValueError("El tipo del Pokémon no puede estar vacío.")

        tipos_validos = {"Normal", "Fuego", "Agua", "Eléctrico", "Planta", "Hielo", "Lucha", "Veneno", "Tierra",
                         "Volador", "Psíquico", "Bicho", "Roca", "Fantasma", "Dragón", "Siniestro", "Acero", "Hada"}

        tipos_ingresados = [t.strip() for t in tipo.split(",")]
        for t in tipos_ingresados:
            if t not in tipos_validos:
                raise ValueError(f"Tipo de Pokémon inválido: {t}")

        stats_db = StatsDB(**stats_data)
        carta_db = CartaPokemonDB(**carta_data)
        carta_db.stats = stats_db

        db.add(carta_db)
        await db.commit()
        await db.refresh(carta_db)

        return carta_db
    except (SQLAlchemyError, ValueError) as e:
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
            stats_id=carta.stats.id if carta.stats else None
        )
        db.add(carta_backup)

        await db.delete(carta)
        await db.commit()
        return carta_backup
    except SQLAlchemyError as e:
        await db.rollback()
        raise  RuntimeError("Error al eliminar carta Pokémon: ") from e

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
