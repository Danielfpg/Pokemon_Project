from base_model import MainModelBase
from typing import Literal
from pydantic import BaseModel, Field
from typing import Literal
from enums import TipoCartaEnum, TipoEnergiaEnum

class CartaEnergia(MainModelBase):
    tipo_carta: Literal["energia"] = Field(default="energia")
    tipo: TipoEnergiaEnum
    especial: bool