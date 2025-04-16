from typing import Annotated, Union
from pydantic import Field
from Models.Model_Pokemon_card import CartaPokemon
from Models.Model_Trainer_card import CartaEntrenador
from Models.Model_Energie_card import CartaEnergia

CartModel = Annotated[
    Union[CartaPokemon, CartaEntrenador, CartaEnergia],
    Field(discriminator="tipo_carta")
]