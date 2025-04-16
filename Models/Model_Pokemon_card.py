from base_model import MainModelBase
from Model_stats import Stats
from enums import TipoCartaEnum
from pydantic import BaseModel, Field
from typing import Literal
class CartaPokemon(MainModelBase):
    tipo_carta: Literal["pokemon"] = Field(default="pokemon")
    tipo: str  # Podrías usar Enum si tienes tipos fijos
    stats: Stats