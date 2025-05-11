from Models.Model_pydantic.base_model import MainModelBase
from Models.enums import TipoCartaEnum
from pydantic import BaseModel, Field
from typing import Literal
class CartaEntrenador(MainModelBase):
    tipo_carta: Literal["entrenador"] = Field(default="entrenador")
    subtipo: str  # Puedes hacer Enum si hay subtipo fijo
    efecto: str
    tiempo: str

    class Config:
        from_attributes = True