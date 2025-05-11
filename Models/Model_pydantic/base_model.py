from pydantic import BaseModel, Field
from Models.enums import RarezaEnum

class MainModelBase(BaseModel):
    id: int
    nombre: str = Field(..., min_length=3, max_length=30)
    rare: RarezaEnum
    costo_en_bolsa: float = Field(..., gt=0)