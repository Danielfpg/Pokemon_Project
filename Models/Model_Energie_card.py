from typing import Literal
from .__init__ import MainModelBase
class CartaEnergia(MainModelBase):
    tipo_carta: Literal["Energia"]
    tipo: str  # fuego, agua, incolora...
    especial: bool