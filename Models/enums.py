from enum import Enum

class TipoCartaEnum(str, Enum):
    pokemon = "Pokemon"
    entrenador = "Entrenador"
    energia = "Energia"

class TipoEnergiaEnum(str, Enum):
    fuego = "fuego"
    agua = "agua"
    planta="planta"
    incolora = "incolora"

class RarezaEnum(str, Enum):
    comun = "común"
    rara = "rara"
    Ultre="Ultre"
    legendaria = "legendaria"