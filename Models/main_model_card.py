from typing import Annotated, Union
from pydantic import Field
from Models.Model_Pokemon_card import CartaPokemonDB
from Models.Model_Trainer_card import CartaEntrenadorDB
from Models.Model_Energie_card import CartaEnergiaDB

CartModel = Annotated[
    Union[CartaPokemonDB, CartaEntrenadorDB, CartaEnergiaDB],
    Field(discriminator="tipo_carta")
]