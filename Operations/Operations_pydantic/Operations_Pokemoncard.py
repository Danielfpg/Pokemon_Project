import csv
from typing import List, Optional
from Models.Model_pydantic.Model_Pokemon_card import CartaPokemon
from Operations.Operations_pydantic.Operations_base import (
    leer_todas_las_cartas,
    buscar_carta_por_nombre,
    write_card_into_csv,
    id_existe,
    column_fields_pokemon,
)

POKEMON_DB = "Pokemon.csv"
BACKUP_DATABASE = "pokemonbackup.csv"


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
    write_card_into_csv(carta, POKEMON_DB, column_fields_pokemon)
    return carta


# Guardar (agregar) carta Pokémon
def agregar_carta_pokemon(carta: CartaPokemon) -> CartaPokemon:
    return crear_carta_pokemon(carta)


# Modificar carta Pokémon
def modificar_carta_pokemon(nombre: str, datos: dict) -> Optional[CartaPokemon]:
    cartas = leer_cartas_pokemon()
    modificada = None

    for i, carta in enumerate(cartas):
        if carta.nombre.lower() == nombre.lower():
            for key, value in datos.items():
                # Evitar modificar el ID (en caso de que se pase el campo 'id')
                if key == "id":
                    continue

                # Verificar si el campo existe en la carta y es modificable
                if hasattr(carta, key):
                    setattr(carta, key, value)
                else:
                    raise ValueError(f"El campo '{key}' no es válido para una carta de Pokémon.")

            modificada = cartas[i]
            break

    # Si se encontró la carta y se hizo alguna modificación, reescribimos el archivo
    if modificada:
        with open(POKEMON_DB, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields_pokemon)
            writer.writeheader()
            for carta in cartas:
                writer.writerow(carta.model_dump())

    return modificada


# Eliminar carta Pokémon (la mueve a backup)
def eliminar_carta_pokemon(nombre: str) -> Optional[CartaPokemon]:
    cartas = leer_cartas_pokemon()
    nuevas = []
    eliminada = None

    for carta in cartas:
        if carta.nombre.lower() == nombre.lower():
            eliminada = carta
        else:
            nuevas.append(carta)

    if eliminada:
        # Escribir en backup
        write_card_into_csv(eliminada, BACKUP_DATABASE, column_fields_pokemon)

        # Reescribir el archivo original sin la carta eliminada
        with open(POKEMON_DB, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields_pokemon)
            writer.writeheader()
            for carta in nuevas:
                writer.writerow(carta.model_dump())
    return eliminada