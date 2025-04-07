from typing import Annotated, Union
from pydantic import BaseModel, Field
from .Model_Pokemon_card import CartaPokemon
from .Model_Trainer_card import CartaEntrenador
from .Model_Energie_card import CartaEnergia


class MainModelBase(BaseModel):
    id: int
    nombre: str = Field(..., min_length=3, max_length=30)
    rare: str = Field(..., min_length=3, max_length=15)
    costo_en_bolsa: float = Field(..., gt=0)



CartModel = Annotated[
    Union[CartaPokemon, CartaEntrenador, CartaEnergia],
    Field(discriminator="tipo_carta")
]