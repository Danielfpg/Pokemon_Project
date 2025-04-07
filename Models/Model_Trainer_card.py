from typing import Literal
from .__init__ import MainModelBase
class CartaEntrenador(MainModelBase):
    tipo_carta: Literal["Entrenador"]
    subtipo: str
    efecto: str
    tiempo: str