from Models.Model_pydantic.base_model import MainModelBase
from Models.Model_pydantic.Model_stats import Stats
from Models.enums import TipoCartaEnum
from pydantic import BaseModel, Field
from typing import Literal,Optional
class CartaPokemonBackup(MainModelBase):
    tipo_carta: Literal["pokemon"] = Field(default="pokemon")
    tipo: str
    stats: Stats

    model_config = {
        "from_attributes": True
    }
