import csv
from typing import List, Optional
from Models.Model_db.Model_Energie_card_db import CartaEnergia
from Operations.Operations_pydantic.Operations_base import (
    leer_todas_las_cartas,
    buscar_carta_por_nombre,
    write_card_into_csv,
    id_existe,
    column_fields_energia,
)

ENERGIA_DB = "Energia.csv"
BACKUP_DATABASE = "Backup.csv"


# Mostrar todas las cartas Energia
def leer_cartas_energia() -> List[CartaEnergia]:
    return [c for c in leer_todas_las_cartas() if isinstance(c, CartaEnergia)]


# Buscar carta Energia por nombre
def buscar_energia_por_nombre(nombre: str) -> Optional[CartaEnergia]:
    carta = buscar_carta_por_nombre(nombre)
    return carta if isinstance(carta, CartaEnergia) else None


# Crear carta Energia
def crear_carta_energia(carta: CartaEnergia) -> CartaEnergia:
    if id_existe(carta.id):
        raise ValueError("Ya existe una carta con ese ID.")
    write_card_into_csv(carta, ENERGIA_DB,column_fields_energia)
    return carta


# Guardar (agregar) carta Energia
def agregar_carta_energia(carta: CartaEnergia) -> CartaEnergia:
    return crear_carta_energia(carta)


# Modificar carta Energia
def modificar_carta_energia(nombre: str, datos: dict) -> Optional[CartaEnergia]:
    cartas = leer_cartas_energia()
    modificada = None

    for i, carta in enumerate(cartas):
        if carta.nombre.lower() == nombre.lower():
            for key, value in datos.items():
                if key == "id":
                    continue
                if hasattr(carta, key):
                    setattr(carta, key, value)
            modificada = cartas[i]
            break

    if modificada:
        with open(ENERGIA_DB, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields_energia)
            writer.writeheader()
            for carta in cartas:
                writer.writerow(carta.model_dump())
    return modificada


# Eliminar carta Energia (la mueve a backup)
def eliminar_carta_energia(nombre: str) -> Optional[CartaEnergia]:
    cartas = leer_cartas_energia()
    nuevas = []
    eliminada = None

    for carta in cartas:
        if carta.nombre.lower() == nombre.lower():
            eliminada = carta
        else:
            nuevas.append(carta)

    if eliminada:
        # Escribir en backup
        write_card_into_csv(eliminada, BACKUP_DATABASE,column_fields_energia)

        # Reescribir el archivo original sin la carta eliminada
        with open(ENERGIA_DB, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields_energia)
            writer.writeheader()
            for carta in nuevas:
                writer.writerow(carta.model_dump())
    return eliminada
