import csv
from typing import List, Optional
from Models.Model_Energie_card import CartaEnergia
from Operations.Operations_base import (
    leer_todas_las_cartas,
    buscar_carta_por_nombre,
    write_card_into_csv,
    id_existe,
)
from .Operations_base import column_fields
DATABASE = "Carts.csv"
BACKUP_DATABASE = "Backup.csv"


# Leer cartas energía
def leer_cartas_energia() -> List[CartaEnergia]:
    return [c for c in leer_todas_las_cartas() if isinstance(c, CartaEnergia)]


# Buscar carta energía
def buscar_energia_por_nombre(nombre: str) -> Optional[CartaEnergia]:
    carta = buscar_carta_por_nombre(nombre)
    return carta if isinstance(carta, CartaEnergia) else None


# Crear carta energía
def crear_carta_energia(carta: CartaEnergia) -> CartaEnergia:
    if id_existe(carta.id):
        raise ValueError("Ya existe una carta con ese ID.")
    write_card_into_csv(carta)
    return carta


# Agregar carta energía
def agregar_carta_energia(carta: CartaEnergia) -> CartaEnergia:
    return crear_carta_energia(carta)


# Modificar carta energía
def modificar_carta_energia(nombre: str, datos: dict) -> Optional[CartaEnergia]:
    cartas = leer_todas_las_cartas()
    modificada = None

    for i, carta in enumerate(cartas):
        if isinstance(carta, CartaEnergia) and carta.nombre.lower() == nombre.lower():
            for key, value in datos.items():
                if key == "id":
                    continue
                if hasattr(carta, key):
                    setattr(carta, key, value)
            modificada = cartas[i]
            break

    if modificada:
        with open(DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields)
            writer.writeheader()
            for carta in cartas:
                writer.writerow(carta.model_dump())
    return modificada


# Eliminar carta energía (backup)
def eliminar_carta_energia(nombre: str) -> Optional[CartaEnergia]:
    cartas = leer_todas_las_cartas()
    nuevas = []
    eliminada = None

    for carta in cartas:
        if isinstance(carta, CartaEnergia) and carta.nombre.lower() == nombre.lower():
            eliminada = carta
        else:
            nuevas.append(carta)

    if eliminada:
        write_card_into_csv(eliminada, BACKUP_DATABASE)
        with open(DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields)
            writer.writeheader()
            for carta in nuevas:
                writer.writerow(carta.model_dump())
    return eliminada
