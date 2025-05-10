from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from base_model import MainModel
from .enums import TipoCartaEnum
from sqlalchemy.orm import relationship
from db.db_connection import Base
from sqlalchemy.orm import validates

class CartaPokemonDB(MainModel,Base):
    __tablename__ = "cartas_Pokemon"
    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.pokemon, nullable=False)
    tipo = Column(String, nullable=False)
    stats_id = Column(Integer, ForeignKey("stats.carta_pokemon_id"), nullable=False)
    stats = relationship("StatsDB", back_populates="carta_pokemon", uselist=False)

    @validates('nombre')
    def validate_nombre(self, key, value):
        if len(value) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return value