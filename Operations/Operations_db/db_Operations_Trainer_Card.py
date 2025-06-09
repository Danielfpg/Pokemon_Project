from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from Models.Model_db.Model_Trainer_card_db import CartaEntrenadorDB
from Models.Model_db.Trainer_Backup import CartaEntrenadorBackupDB
from Models.Model_pydantic.Model_Trainer_card import CartaEntrenador
import unicodedata
import csv
import os

TRAINER_CSV = "Entrenador.csv"
TRAINER_BACKUP_CSV = "Entrenadorbackup.csv"

TRAINER_HEADERS = ["id", "nombre", "rare", "costo_en_bolsa", "tipo_carta", "subtipo", "efecto", "tiempo"]

async def crear_carta_entrenador(db: AsyncSession, carta: CartaEntrenador):
    carta_db = CartaEntrenadorDB(**carta.dict())
    db.add(carta_db)
    await db.commit()
    await db.refresh(carta_db)

    # Guardar en Entrenador.csv
    archivo_existe = os.path.exists(TRAINER_CSV)
    with open(TRAINER_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=TRAINER_HEADERS)
        if not archivo_existe or os.stat(TRAINER_CSV).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "id": carta_db.id,
            "nombre": carta_db.nombre,
            "rare": carta_db.rare,
            "costo_en_bolsa": carta_db.costo_en_bolsa,
            "tipo_carta": carta_db.tipo_carta,
            "subtipo": carta_db.subtipo,
            "efecto": carta_db.efecto,
            "tiempo": carta_db.tiempo
        })

    return carta_db


async def obtener_cartas_entrenador(db: AsyncSession):
    result = await db.execute(select(CartaEntrenadorDB))
    return result.scalars().all()

async def obtener_carta_entrenador_por_nombre(db: AsyncSession, nombre: str):
    nombre = nombre.strip()
    result = await db.execute(select(CartaEntrenadorDB))
    cartas = result.scalars().all()
    for carta in cartas:
        if carta.nombre.strip().lower() == nombre.lower():
            return carta
    return None


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

    # Guardar en Entrenadorbackup.csv
    archivo_existe = os.path.exists(TRAINER_BACKUP_CSV)
    with open(TRAINER_BACKUP_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=TRAINER_HEADERS)
        if not archivo_existe:
            writer.writeheader()
        writer.writerow({
            "id": carta.id,
            "nombre": carta.nombre,
            "rare": carta.rare,
            "costo_en_bolsa": carta.costo_en_bolsa,
            "tipo_carta": carta.tipo_carta,
            "subtipo": carta.subtipo,
            "efecto": carta.efecto,
            "tiempo": carta.tiempo
        })

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

    # 1. Eliminar de Entrenadorbackup.csv
    if os.path.exists(TRAINER_BACKUP_CSV):
        with open(TRAINER_BACKUP_CSV, newline='', encoding='utf-8') as archivo:
            filas = list(csv.DictReader(archivo))

        nuevas_filas = [fila for fila in filas if fila["nombre"] != nombre]

        with open(TRAINER_BACKUP_CSV, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=TRAINER_HEADERS)
            writer.writeheader()
            writer.writerows(nuevas_filas)

    # 2. Agregar a Entrenador.csv
    archivo_existe = os.path.exists(TRAINER_CSV)
    with open(TRAINER_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=TRAINER_HEADERS)
        if not archivo_existe or os.stat(TRAINER_CSV).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "id": carta_restaurada.id,
            "nombre": carta_restaurada.nombre,
            "rare": carta_restaurada.rare,
            "costo_en_bolsa": carta_restaurada.costo_en_bolsa,
            "tipo_carta": carta_restaurada.tipo_carta,
            "subtipo": carta_restaurada.subtipo,
            "efecto": carta_restaurada.efecto,
            "tiempo": carta_restaurada.tiempo
        })

    return carta_restaurada

