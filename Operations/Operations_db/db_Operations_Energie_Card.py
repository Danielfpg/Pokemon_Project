from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models.Model_db.Model_Energie_card_db import CartaEnergiaDB
from Models.Model_db.Energie_Backup import CartaEnergiaBackupDB
from Models.Model_pydantic.Model_Energie_card import CartaEnergia
import csv
import os

ENERGIA_CSV = "Energia.csv"
ENERGIA_BACKUP_CSV = "Energiebackup.csv"

ENERGIA_HEADERS = ["id", "nombre", "rare", "costo_en_bolsa", "tipo_carta", "tipo", "especial"]
async def crear_carta_energia(db: AsyncSession, carta: CartaEnergia):
    carta_db = CartaEnergiaDB(**carta.dict())
    db.add(carta_db)
    await db.commit()
    await db.refresh(carta_db)

    # Guardar en Energia.csv
    archivo_existe = os.path.exists(ENERGIA_CSV)
    with open(ENERGIA_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=ENERGIA_HEADERS)
        if not archivo_existe or os.stat(ENERGIA_CSV).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "id": carta_db.id,
            "nombre": carta_db.nombre,
            "rare": carta_db.rare,
            "costo_en_bolsa": carta_db.costo_en_bolsa,
            "tipo_carta": carta_db.tipo_carta,
            "tipo": carta_db.tipo,
            "especial": carta_db.especial
        })

    return carta_db

async def obtener_cartas_energia(db: AsyncSession):
    result = await db.execute(select(CartaEnergiaDB))
    return result.scalars().all()

async def obtener_carta_energia_por_nombre(db: AsyncSession, nombre: str):
    nombre = nombre.strip()
    result = await db.execute(select(CartaEnergiaDB))
    cartas = result.scalars().all()
    for carta in cartas:
        if carta.nombre.strip().lower() == nombre.lower():
            return carta
    return None

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

    # Guardar en Energiebackup.csv
    archivo_existe = os.path.exists(ENERGIA_BACKUP_CSV)
    with open(ENERGIA_BACKUP_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=ENERGIA_HEADERS)
        if not archivo_existe or os.stat(ENERGIA_BACKUP_CSV).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "id": backup.id,
            "nombre": backup.nombre,
            "rare": backup.rare,
            "costo_en_bolsa": backup.costo_en_bolsa,
            "tipo_carta": backup.tipo_carta,
            "tipo": backup.tipo,
            "especial": backup.especial
        })

    return backup


async def restaurar_carta_energia(db: AsyncSession, nombre: str):
    result = await db.execute(
        select(CartaEnergiaBackupDB).where(CartaEnergiaBackupDB.nombre == nombre)
    )
    backup = result.scalars().first()
    if not backup:
        return None

    # Restaurar en la base de datos
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

    # Limpiar del CSV de backup
    if os.path.exists(ENERGIA_BACKUP_CSV):
        with open(ENERGIA_BACKUP_CSV, mode="r", newline="", encoding="utf-8") as archivo:
            filas = list(csv.DictReader(archivo))

        nuevas_filas = [fila for fila in filas if fila["nombre"] != nombre]

        with open(ENERGIA_BACKUP_CSV, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=ENERGIA_HEADERS)
            writer.writeheader()
            writer.writerows(nuevas_filas)

    return carta_restaurada


