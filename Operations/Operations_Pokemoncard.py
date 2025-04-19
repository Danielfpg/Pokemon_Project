import csv
from typing import List, Optional
from Models.Model_Pokemon_card import CartaPokemon
from Operations.Operations_base import (
    leer_todas_las_cartas,
    buscar_carta_por_nombre,
    write_card_into_csv,
    id_existe,
)
from .Operations_base import column_fields

DATABASE = "Carts.csv"
BACKUP_DATABASE = "Backup.csv"


# Mostrar todas las cartas Pokémon
def leer_cartas_pokemon() -> List[CartaPokemon]:
    return [c for c in leer_todas_las_cartas() if isinstance(c, CartaPokemon)]


# Buscar carta Pokémon por nombre
def buscar_pokemon_por_nombre(nombre: str) -> Optional[CartaPokemon]:
    carta = buscar_carta_por_nombre(nombre)
    return carta if isinstance(carta, CartaPokemon) else None


# Crear carta Pokémon
def crear_carta_pokemon(carta: CartaPokemon) -> CartaPokemon:
    if id_existe(carta.id):
        raise ValueError("Ya existe una carta con ese ID.")
    print("DEBUG: Se está usando esta versión de crear_carta_pokemon")
    print("DEBUG: Archivo destino:", DATABASE)
    write_card_into_csv(carta, DATABASE)
    return carta


# Guardar (agregar) carta Pokémon
def agregar_carta_pokemon(carta: CartaPokemon) -> CartaPokemon:
    return crear_carta_pokemon(carta)


# Modificar carta Pokémon
def modificar_carta_pokemon(nombre: str, datos: dict) -> Optional[CartaPokemon]:
    cartas = leer_todas_las_cartas()
    modificada = None

    for i, carta in enumerate(cartas):
        if isinstance(carta, CartaPokemon) and carta.nombre.lower() == nombre.lower():
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


# Eliminar carta Pokémon (la mueve a backup)
def eliminar_carta_pokemon(nombre: str) -> Optional[CartaPokemon]:
    cartas = leer_todas_las_cartas()
    nuevas = []
    eliminada = None

    for carta in cartas:
        if isinstance(carta, CartaPokemon) and carta.nombre.lower() == nombre.lower():
            eliminada = carta
        else:
            nuevas.append(carta)

    if eliminada:
        # Escribir en backup
        write_card_into_csv(eliminada, BACKUP_DATABASE)

        # Reescribir el archivo original sin la carta eliminada
        with open(DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields)
            writer.writeheader()
            for carta in nuevas:
                writer.writerow(carta.model_dump())
    return eliminada
