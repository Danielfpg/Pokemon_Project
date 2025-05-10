from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models.Model_Trainer_card import CartaEntrenadorDB
from Models.Trainer_Backup import CartaEntrenadorBackupDB

async def crear_carta_entrenador(db: AsyncSession, carta: CartaEntrenadorDB):
    db.add(carta)
    await db.commit()
    await db.refresh(carta)
    return carta

async def obtener_cartas_entrenador(db: AsyncSession):
    result = await db.execute(select(CartaEntrenadorDB))
    return result.scalars().all()

async def obtener_carta_entrenador_por_nombre(db: AsyncSession, nombre: str):
    result = await db.execute(
        select(CartaEntrenadorDB).where(CartaEntrenadorDB.nombre == nombre)
    )
    return result.scalars().first()

async def modificar_carta_entrenador(db: AsyncSession, nombre: str, datos_actualizados: dict):
    carta = await obtener_carta_entrenador_por_nombre(db, nombre)
    if not carta:
        return None

    for key, value in datos_actualizados.items():
        if hasattr(carta, key) and key != "id":
            setattr(carta, key, value)

    await db.commit()
    await db.refresh(carta)
    return carta

async def eliminar_carta_entrenador(db: AsyncSession, nombre: str):
    carta = await obtener_carta_entrenador_por_nombre(db, nombre)
    if not carta:
        return None

    backup = CartaEntrenadorBackupDB(
        id=carta.id,
        nombre=carta.nombre,
        rare=carta.rare,
        costo_en_bolsa=carta.costo_en_bolsa,
        tipo_carta=carta.tipo_carta,
        subtipo=carta.subtipo,
        efecto=carta.efecto,
        tiempo=carta.tiempo
    )

    db.add(backup)
    await db.delete(carta)
    await db.commit()
    return backup

async def restaurar_carta_entrenador(db: AsyncSession, nombre: str):
    result = await db.execute(
        select(CartaEntrenadorBackupDB).where(CartaEntrenadorBackupDB.nombre == nombre)
    )
    backup = result.scalars().first()
    if not backup:
        return None

    carta_restaurada = CartaEntrenadorDB(
        id=backup.id,
        nombre=backup.nombre,
        rare=backup.rare,
        costo_en_bolsa=backup.costo_en_bolsa,
        tipo_carta=backup.tipo_carta,
        subtipo=backup.subtipo,
        efecto=backup.efecto,
        tiempo=backup.tiempo
    )

    db.add(carta_restaurada)
    await db.delete(backup)
    await db.commit()
    await db.refresh(carta_restaurada)
    return carta_restaurada
