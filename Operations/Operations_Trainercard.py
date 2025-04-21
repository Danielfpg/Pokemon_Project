import csv
from typing import List, Optional
from Models.Model_Trainer_card import CartaEntrenador
from Operations.Operations_base import (
    leer_todas_las_cartas,
    buscar_carta_por_nombre,
    write_card_into_csv,
    id_existe,
    column_fields_entrenador,
)

ENTRENADOR_DB = "Entrenador.csv"
BACKUP_DATABASE = "Backup.csv"


# Leer cartas entrenador
def leer_cartas_entrenador() -> List[CartaEntrenador]:
    return [c for c in leer_todas_las_cartas() if isinstance(c, CartaEntrenador)]


# Buscar carta entrenador
def buscar_entrenador_por_nombre(nombre: str) -> Optional[CartaEntrenador]:
    carta = buscar_carta_por_nombre(nombre)
    return carta if isinstance(carta, CartaEntrenador) else None


# Crear carta entrenador
def crear_carta_entrenador(carta: CartaEntrenador) -> CartaEntrenador:
    if id_existe(carta.id):
        raise ValueError("Ya existe una carta con ese ID.")
    write_card_into_csv(carta, ENTRENADOR_DB,column_fields_entrenador)
    return carta


# Agregar carta entrenador
def agregar_carta_entrenador(carta: CartaEntrenador) -> CartaEntrenador:
    return crear_carta_entrenador(carta)


# Modificar carta entrenador
def modificar_carta_entrenador(nombre: str, datos: dict) -> Optional[CartaEntrenador]:
    cartas = leer_cartas_entrenador()
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


    if modificada:
        with open(ENTRENADOR_DB, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields_entrenador)
            writer.writeheader()
            for carta in cartas:
                writer.writerow(carta.model_dump())
    return modificada


# Eliminar carta entrenador (backup)
def eliminar_carta_entrenador(nombre: str) -> Optional[CartaEntrenador]:
    cartas = leer_cartas_entrenador()
    nuevas = []
    eliminada = None

    for carta in cartas:
        if carta.nombre.lower() == nombre.lower():
            eliminada = carta
        else:
            nuevas.append(carta)

    if eliminada:
        write_card_into_csv(eliminada, BACKUP_DATABASE,column_fields_entrenador)
        with open(ENTRENADOR_DB, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields_entrenador)
            writer.writeheader()
            for carta in nuevas:
                writer.writerow(carta.model_dump())
    return eliminada
