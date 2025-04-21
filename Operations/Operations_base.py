import csv
import ast
from typing import Optional, List
from Models.main_model_card import CartModel
from Models.base_model import MainModelBase
from Models.Model_Pokemon_card import CartaPokemon
from Models.Model_Energie_card import CartaEnergia
from Models.Model_Trainer_card import CartaEntrenador

# Archivos de bases de datos
DATABASES = {
    "pokemon": "Pokemon.csv",
    "entrenador": "Entrenador.csv",
    "energia": "Energia.csv",
}
BACKUP_DATABASE = "Backup.csv"

# Define los campos de columna específicos para cada tipo de carta
column_fields_pokemon = ["id", "nombre", "tipo_carta", "rare", "costo_en_bolsa", "tipo", "especial", "subtipo",
                         "efecto", "tiempo", "stats"]
column_fields_entrenador = ["id", "nombre", "tipo_carta", "rare", "costo_en_bolsa", "subtipo","especial",
                            "efecto", "tiempo"]
column_fields_energia = ["id", "nombre", "tipo_carta", "rare", "costo_en_bolsa", "tipo", "especial"]


def leer_csv(filename: str) -> List[dict]:
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def convertir_stats(row: dict) -> dict:
    if "stats" in row and row["stats"]:
        try:
            row["stats"] = ast.literal_eval(row["stats"])
        except Exception as e:
            print("Error convirtiendo stats:", e)
            row["stats"] = {}
    return row


def validar_y_completar_fila(row: dict, tipo: str) -> dict:
    # Asigna los valores por defecto a los campos dependiendo del tipo de carta
    if tipo == "pokemon":
        column_fields = column_fields_pokemon
    elif tipo == "entrenador":
        column_fields = column_fields_entrenador
    else:  # Asume que es de tipo energia
        column_fields = column_fields_energia

    for field in column_fields:
        row.setdefault(field, "")
    return row


def crear_carta_por_tipo(tipo: str, row: dict) -> CartModel:
    if tipo == "pokemon":
        return CartaPokemon(**row)
    elif tipo == "entrenador":
        return CartaEntrenador(**row)
    elif tipo == "energia":
        return CartaEnergia(**row)
    return None


def leer_todas_las_cartas() -> List[MainModelBase]:
    cartas = []
    for tipo, archivo in DATABASES.items():
        for row in leer_csv(archivo):
            row = validar_y_completar_fila(row, tipo)
            if "tipo_carta" not in row or not row["tipo_carta"]:
                continue
            row = convertir_stats(row)
            carta = crear_carta_por_tipo(tipo, row)
            if carta:
                cartas.append(carta)
    return cartas


def filtrar_cartas_por_tipo(tipo: str) -> List[CartModel]:
    tipo = tipo.lower()
    todas = leer_todas_las_cartas()
    return [carta for carta in todas if getattr(carta, "tipo_carta", "").lower() == tipo]


def buscar_carta_por_nombre(nombre: str) -> Optional[CartModel]:
    cartas = leer_todas_las_cartas()
    for carta in cartas:
        if carta.nombre.lower() == nombre.lower():
            return carta
    return None


def id_existe(id: int) -> bool:
    for archivo in DATABASES.values():
        try:
            with open(archivo, newline="") as f:
                reader = csv.DictReader(f)
                # Asegurarse de que hay encabezado
                if not reader.fieldnames or 'id' not in reader.fieldnames:
                    continue
                if any(int(row["id"]) == id for row in reader if row["id"].isdigit()):
                    return True
        except Exception as e:
            print(f"Error verificando ID en {archivo}: {e}")
    return False



def write_card_into_csv(card: CartModel, filename: str, column_fields: List[str]):
    data = card.model_dump()
    if "stats" in data and isinstance(data["stats"], dict):
        data["stats"] = str(data["stats"])
    for field in column_fields:
        data.setdefault(field, "")
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=column_fields)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)


def new_card(card: CartModel) -> CartModel:
    if id_existe(card.id):
        raise ValueError("Ya existe una carta con ese ID.")
    tipo = card.tipo_carta.lower()
    archivo = DATABASES.get(tipo)
    if not archivo:
        raise ValueError(f"Tipo de carta no reconocido: {tipo}")

    # Determina los campos de columna según el tipo
    if tipo == "pokemon":
        column_fields = column_fields_pokemon
    elif tipo == "entrenador":
        column_fields = column_fields_entrenador
    else:  # Asume que es de tipo energia
        column_fields = column_fields_energia

    write_card_into_csv(card, archivo, column_fields)
    return card


def agregar_carta(carta: CartModel) -> CartModel:
    return new_card(carta)


def modificar_carta(nombre: str, data: dict) -> Optional[CartModel]:
    for tipo, archivo in DATABASES.items():
        cartas = []
        modificada = None
        with open(archivo, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row = convertir_stats(row)
                row = validar_y_completar_fila(row, tipo)
                carta = crear_carta_por_tipo(tipo, row)
                if carta.nombre.lower() == nombre.lower():
                    for key, value in data.items():
                        if key != "id" and hasattr(carta, key):
                            setattr(carta, key, value)
                    modificada = carta
                    cartas.append(carta)
                else:
                    cartas.append(carta)

        if modificada:
            # Escribe el archivo con la carta modificada
            if tipo == "pokemon":
                column_fields = column_fields_pokemon
            elif tipo == "entrenador":
                column_fields = column_fields_entrenador
            else:
                column_fields = column_fields_energia

            with open(archivo, mode="w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=column_fields)
                writer.writeheader()
                for carta in cartas:
                    writer.writerow(carta.model_dump())
            return modificada

    return None


def eliminar_carta(nombre: str) -> Optional[CartModel]:
    for tipo, archivo in DATABASES.items():
        cartas = []
        eliminada = None
        with open(archivo, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row = convertir_stats(row)
                row = validar_y_completar_fila(row, tipo)
                carta = crear_carta_por_tipo(tipo, row)
                if carta.nombre.lower() == nombre.lower():
                    eliminada = carta
                    write_card_into_csv(carta, BACKUP_DATABASE,
                                        column_fields_pokemon if tipo == "pokemon" else column_fields_entrenador if tipo == "entrenador" else column_fields_energia)
                else:
                    cartas.append(carta)

        if eliminada:
            with open(archivo, mode="w", newline="") as f:
                writer = csv.DictWriter(f,
                                        fieldnames=column_fields_pokemon if tipo == "pokemon" else column_fields_entrenador if tipo == "entrenador" else column_fields_energia)
                writer.writeheader()
                for carta in cartas:
                    writer.writerow(carta.model_dump())
            return eliminada

    return None


def restaurar_carta(nombre: str) -> Optional[CartModel]:
    cartas_backup = leer_csv(BACKUP_DATABASE)
    restaurada = None
    nuevas_backup = []

    for row in cartas_backup:
        if row["nombre"].lower() == nombre.lower():
            row = convertir_stats(row)
            tipo = row["tipo_carta"].lower()
            carta = crear_carta_por_tipo(tipo, row)
            if carta:
                archivo = DATABASES.get(tipo)
                if archivo:
                    write_card_into_csv(carta, archivo,
                                        column_fields_pokemon if tipo == "pokemon" else column_fields_entrenador if tipo == "entrenador" else column_fields_energia)
                    restaurada = carta
        else:
            nuevas_backup.append(row)

    if restaurada:
        with open(BACKUP_DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f,
                                    fieldnames=column_fields_pokemon if tipo == "pokemon" else column_fields_entrenador if tipo == "entrenador" else column_fields_energia)
            writer.writeheader()
            for row in nuevas_backup:
                writer.writerow(row)

    return restaurada
