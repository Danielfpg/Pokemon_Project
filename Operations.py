import csv
from typing import Optional, List
from Models.main_model_card import CartModel, MainModelBase
from Models.Model_Pokemon_card import CartaPokemon
from Models.Model_Energie_card import CartaEnergia
from Models.Model_Trainer_card import CartaEntrenador

DATABASE = "Carts.csv"
column_fields = ["id", "nombre", "tipo_carta", "rare", "costo_en_bolsa",
                 "tipo", "especial", "subtipo", "efecto", "tiempo", "stats"]


#Mostrar todas las cartas
def leer_todas_las_cartas() -> List[MainModelBase]:
    with open(DATABASE, newline="") as f:
        reader = csv.DictReader(f)
        cartas = []
        for row in reader:
            tipo = row["tipo_carta"]
            if tipo == "Pokemon":
                cartas.append(CartaPokemon(**row))
            elif tipo == "Entrenador":
                cartas.append(CartaEntrenador(**row))
            elif tipo == "Energia":
                cartas.append(CartaEnergia(**row))
        return cartas

#Filtrar por tipo de carta
def filtrar_cartas_por_tipo(tipo: str) -> List[CartModel]:
    tipo = tipo.lower()
    todas = leer_todas_las_cartas()
    return [carta for carta in todas if getattr(carta, "tipo_carta", "").lower() == tipo]

#Mostrar carta por nombre
def buscar_carta_por_nombre(nombre: str) -> Optional[CartModel]:
    cartas = leer_todas_las_cartas()
    for carta in cartas:
        if carta.nombre.lower() == nombre.lower():
            return carta
    return None


def id_existe(id: int) -> bool:
    try:
        with open(DATABASE, newline="") as f:
            reader = csv.DictReader(f)
            return any(int(row["id"]) == id for row in reader)
    except FileNotFoundError:
        return False


#Guardar carta en CSV
def write_card_into_csv(card: CartModel):
    # Convierte stats en texto si existen
    data = card.model_dump()
    if "stats" in data and isinstance(data["stats"], dict):
        data["stats"] = str(data["stats"])  # guardar como string simple

    # Asegura que todos los campos estén presentes, aunque sea en blanco
    for field in column_fields:
        data.setdefault(field, "")

    with open(DATABASE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=column_fields)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)



#Crear una carta
def new_card(card: CartModel) -> CartModel:
    if id_existe(card.id):
        raise ValueError("Ya existe una carta con ese ID.")
    write_card_into_csv(card)
    return card

#Agragar carta
def agregar_carta(carta: CartModel) -> CartModel:
    return new_card(carta)

#Modificar carta
def modificar_carta(nombre: str, data: dict) -> Optional[CartModel]:
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
        with open(DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields)
            writer.writeheader()
            for carta in cartas:
                writer.writerow(carta.model_dump())

    return modificado
#Borrar carta
def eliminar_carta(nombre: str) -> Optional[CartModel]:
    cartas = leer_todas_las_cartas()
    eliminada = None
    nuevas = []
    for carta in cartas:
        if carta.nombre.lower() == nombre.lower():
            eliminada = carta
        else:
            nuevas.append(carta)
    if eliminada:
        with open(DATABASE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=column_fields)
            writer.writeheader()
            for carta in nuevas:
                writer.writerow(carta.model_dump())
    return eliminada
