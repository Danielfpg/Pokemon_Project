from typing import List, Optional, Dict, Any
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from Models.Model_Trainer_card import CartaEntrenador
from Operations.Operations_base import write_card_into_csv, leer_todas_las_cartas
import csv

# Leer todas las cartas Entrenador
async def leer_cartas_entrenador_sql(session: AsyncSession) -> List[CartaEntrenador]:
    query = select(CartaEntrenador)
    result = await session.exec(query)
    return result.all()

# Buscar carta Entrenador por nombre
async def buscar_entrenador_por_nombre_sql(session: AsyncSession, nombre: str) -> Optional[CartaEntrenador]:
    query = select(CartaEntrenador).where(CartaEntrenador.nombre == nombre)
    result = await session.exec(query)
    return result.first()

# Crear carta Entrenador
async def crear_carta_entrenador_sql(session: AsyncSession, carta: CartaEntrenador) -> CartaEntrenador:
    session.add(carta)
    await session.commit()
    await session.refresh(carta)
    return carta

# Modificar carta Entrenador
async def modificar_carta_entrenador_sql(session: AsyncSession, nombre: str, datos: Dict[str, Any]) -> Optional[CartaEntrenador]:
    carta = await buscar_entrenador_por_nombre_sql(session, nombre)
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

BACKUP_DATABASE = "Backup.csv"
DATABASE = "Carts.csv"
column_fields = ["id", "nombre", "tipo_carta", "subtipo", "efecto", "tiempo"]

# Eliminar carta Entrenador (trasladar a Backup.csv y eliminar de Carts.csv)
async def eliminar_carta_entrenador_sql(session: AsyncSession, nombre: str) -> Optional[CartaEntrenador]:
    # Buscar la carta por nombre
    carta = await buscar_entrenador_por_nombre_sql(session, nombre)
    if carta is None:
        return None

    # Leer todas las cartas actuales
    cartas = leer_todas_las_cartas()

    # Filtrar las cartas que no son la que vamos a eliminar
    nuevas_cartas = [c for c in cartas if not (isinstance(c, CartaEntrenador) and c.nombre.lower() == nombre.lower())]

    # Guardar la carta eliminada en Backup.csv
    write_card_into_csv(carta, BACKUP_DATABASE)

    # Reescribir el archivo Carts.csv sin la carta eliminada
    with open(DATABASE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=column_fields)
        writer.writeheader()
        for carta in nuevas_cartas:
            writer.writerow(carta.model_dump())  # Asegúrate de que model_dump() se use correctamente
    return carta
