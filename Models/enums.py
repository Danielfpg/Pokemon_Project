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
    comun = "comun"
    rara = "rara"
    Ultra="Ultra"
    legendaria = "legendaria"