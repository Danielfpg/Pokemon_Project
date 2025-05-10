from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models.Model_Energie_card import CartaEnergiaDB
from Models.Energie_Backup import CartaEnergiaBackupDB

async def crear_carta_energia(db: AsyncSession, carta: CartaEnergiaDB):
    db.add(carta)
    await db.commit()
    await db.refresh(carta)
    return carta

async def obtener_cartas_energia(db: AsyncSession):
    result = await db.execute(select(CartaEnergiaDB))
    return result.scalars().all()

async def obtener_carta_energia_por_nombre(db: AsyncSession, nombre: str):
    result = await db.execute(
        select(CartaEnergiaDB).where(CartaEnergiaDB.nombre == nombre)
    )
    return result.scalars().first()

async def modificar_carta_energia(db: AsyncSession, nombre: str, datos_actualizados: dict):
    carta = await obtener_carta_energia_por_nombre(db, nombre)
    if not carta:
        return None

    for key, value in datos_actualizados.items():
        if hasattr(carta, key) and key != "id":
            setattr(carta, key, value)

    await db.commit()
    await db.refresh(carta)
    return carta

async def eliminar_carta_energia(db: AsyncSession, nombre: str):
    carta = await obtener_carta_energia_por_nombre(db, nombre)
    if not carta:
        return None

    backup = CartaEnergiaBackupDB(
        id=carta.id,
        nombre=carta.nombre,
        rare=carta.rare,
        costo_en_bolsa=carta.costo_en_bolsa,
        tipo_carta=carta.tipo_carta,
        tipo=carta.tipo,
        especial=carta.especial
    )

    db.add(backup)
    await db.delete(carta)
    await db.commit()
    return backup

async def restaurar_carta_energia(db: AsyncSession, nombre: str):
    result = await db.execute(
        select(CartaEnergiaBackupDB).where(CartaEnergiaBackupDB.nombre == nombre)
    )
    backup = result.scalars().first()
    if not backup:
        return None

    carta_restaurada = CartaEnergiaDB(
        id=backup.id,
        nombre=backup.nombre,
        rare=backup.rare,
        costo_en_bolsa=backup.costo_en_bolsa,
        tipo_carta=backup.tipo_carta,
        tipo=backup.tipo,
        especial=backup.especial
    )

    db.add(carta_restaurada)
    await db.delete(backup)
    await db.commit()
    await db.refresh(carta_restaurada)
    return carta_restaurada
