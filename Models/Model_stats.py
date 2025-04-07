from pydantic import BaseModel, Field

class Stats(BaseModel):
    speed: int = Field(..., ge=0)
    hp: int = Field(..., ge=0)
    attack: int = Field(..., ge=0)
    defense: int = Field(..., ge=0)
    special_atk: int = Field(..., ge=0)
    special_def: int = Field(..., ge=0)
