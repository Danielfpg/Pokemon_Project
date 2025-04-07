from typing import Literal
from .__init__ import MainModelBase,Stats

class CartaPokemon(MainModelBase):
    tipo_carta: Literal["Pokemon"]
    tipo: str
    stats: Stats