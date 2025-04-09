from enum import Enum

class TipoCartaEnum(str, Enum):
    pokemon = "Pokemon"
    entrenador = "Entrenador"
    energia = "Energia"

class TipoEnergiaEnum(str, Enum):
    fuego = "fuego"
    agua = "agua"
    incolora = "incolora"

class RarezaEnum(str, Enum):
    comun = "común"
    rara = "rara"
    legendaria = "legendaria"