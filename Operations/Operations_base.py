import csv
import ast
from typing import Optional, List
from Models.main_model_card import CartModel
from Models.base_model import MainModelBase
from Models.Model_Pokemon_card import CartaPokemon
from Models.Model_Energie_card import CartaEnergia
from Models.Model_Trainer_card import CartaEntrenador

DATABASE = "Carts.csv"
BACKUP_DATABASE = "Backup.csv"
column_fields = ["id", "nombre", "tipo_carta", "rare", "costo_en_bolsa",
                 "tipo", "especial", "subtipo", "efecto", "tiempo", "stats"]


# ---------------------------- Helper Functions ----------------------------

def leer_csv(filename: str) -> List[dict]:
    """Lee el archivo CSV y retorna su contenido como una lista de diccionarios."""
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def convertir_stats(row: dict) -> dict:
    """Convierte la columna 'stats' en un diccionario si es necesario."""
    if "stats" in row and row["stats"]:
        try:
            row["stats"] = ast.literal_eval(row["stats"])
        except Exception as e:
            print("Error convirtiendo stats:", e)
            row["stats"] = {}
    return row


def crear_carta_por_tipo(tipo: str, row: dict) -> CartModel:
    """Crea una carta del tipo correspondiente según el tipo de carta."""
    if tipo == "pokemon":
        return CartaPokemon(**row)
    elif tipo == "entrenador":
        return CartaEntrenador(**row)
    elif tipo == "energia":
        return CartaEnergia(**row)
    return None


# ---------------------------- CRUD Operations ----------------------------

def leer_todas_las_cartas() -> List[MainModelBase]:
    """Lee todas las cartas del archivo CSV y las devuelve como una lista de instancias de cartas."""
    cartas = []
    for row in leer_csv(DATABASE):
        row = convertir_stats(row)  # Convierte 'stats' si existe
        tipo = row["tipo_carta"].lower()  # Determina el tipo de carta
        carta = crear_carta_por_tipo(tipo, row)
        if carta:
            cartas.append(carta)
    return cartas


def filtrar_cartas_por_tipo(tipo: str) -> List[CartModel]:
    """Filtra las cartas por tipo."""
    tipo = tipo.lower()
    todas = leer_todas_las_cartas()
    return [carta for carta in todas if getattr(carta, "tipo_carta", "").lower() == tipo]


def buscar_carta_por_nombre(nombre: str) -> Optional[CartModel]:
    """Busca una carta por su nombre."""
    cartas = leer_todas_las_cartas()
    for carta in cartas:
        if carta.nombre.lower() == nombre.lower():
            return carta
    return None


def id_existe(id: int) -> bool:
    """Verifica si una carta con el ID especificado ya existe."""
    try:
        with open(DATABASE, newline="") as f:
            reader = csv.DictReader(f)
            return any(int(row["id"]) == id for row in reader)
    except FileNotFoundError:
        return False


def write_card_into_csv(card: CartModel, filename: str):
    """Escribe una carta en el archivo CSV especificado."""
    data = card.model_dump()
    # Convierte 'stats' en texto si es un diccionario
    if "stats" in data and isinstance(data["stats"], dict):
        data["stats"] = str(data["stats"])

    # Asegura que todos los campos estén presentes, incluso si están vacíos
    for field in column_fields:
        data.setdefault(field, "")

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=column_fields)
        if file.tell() == 0:
            writer.writeheader()  # Escribe los encabezados solo si el archivo está vacío
        writer.writerow(data)


def new_card(card: CartModel) -> CartModel:
    """Crea una nueva carta, asegurándose de que no exista una carta con el mismo ID."""
    if id_existe(card.id):
        raise ValueError("Ya existe una carta con ese ID.")
    write_card_into_csv(card, DATABASE)
    return card


def agregar_carta(carta: CartModel) -> CartModel:
    """Agrega una carta al archivo CSV."""
    return new_card(carta)


def modificar_carta(nombre: str, data: dict) -> Optional[CartModel]:
    """Modifica una carta existente por su nombre."""
    cartas = leer_todas_las_cartas()
    modificado = None

    for i, carta in enumerate(cartas):
        if carta.nombre.lower() == nombre.lower():
            for key, value in data.items():
                if key == "id":
                    continue  # No permitir modificar el ID
                if hasattr(cartas[i], key):
                    setattr(cartas[i], key, value)
            modificado = cartas[i]
            break

    if modificado:
        # Sobrescribe el archivo CSV con las cartas modificadas
        with open(DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields)
            writer.writeheader()
            for carta in cartas:
                writer.writerow(carta.model_dump())

    return modificado


def eliminar_carta(nombre: str) -> Optional[CartModel]:
    """Elimina una carta por su nombre, moviéndola a un archivo de respaldo."""
    cartas = leer_todas_las_cartas()
    eliminada = None
    nuevas = []

    for carta in cartas:
        if carta.nombre.lower() == nombre.lower():
            eliminada = carta
            write_card_into_csv(carta, BACKUP_DATABASE)  # Mueve la carta al Backup.csv
        else:
            nuevas.append(carta)

    if eliminada:
        # Sobrescribe el archivo CSV con las cartas restantes
        with open(DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields)
            writer.writeheader()
            for carta in nuevas:
                writer.writerow(carta.model_dump())
        print(f"Intentando eliminar la carta con nombre: {nombre} y moverla a backup")

    return eliminada


def restaurar_carta_desde_backup(nombre: str) -> Optional[CartModel]:
    """Restaura una carta desde el archivo de respaldo (Backup) al archivo principal (Carts)."""
    cartas_backup = leer_csv(BACKUP_DATABASE)
    restaurada = None
    nuevas_backup = []

    for row in cartas_backup:
        if row["nombre"].lower() == nombre.lower():
            row = convertir_stats(row)
            tipo = row["tipo_carta"].lower()
            carta = crear_carta_por_tipo(tipo, row)
            if carta:
                write_card_into_csv(carta, DATABASE)  # Restaura la carta a Carts.csv
                restaurada = carta
        else:
            nuevas_backup.append(row)

    # Sobrescribe el archivo de respaldo sin la carta restaurada
    if restaurada:
        with open(BACKUP_DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields)
            writer.writeheader()
            for row in nuevas_backup:
                writer.writerow(row)

    return restaurada
