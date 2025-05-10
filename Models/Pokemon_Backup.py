from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from base_model import MainModel
from .enums import TipoCartaEnum
from sqlalchemy.orm import relationship
from db.db_connection import Base


class CartaPokemonBackupDB(MainModel, Base):
    __tablename__ = "cartas_pokemon_backup"

    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.pokemon, nullable=False)
    tipo = Column(String, nullable=False)
    stats_id = Column(Integer, ForeignKey("stats.carta_pokemon_id"),
                      nullable=True)  # Puede estar en backup sin stats relacionados
    stats = relationship("StatsDB", back_populates="carta_pokemon_backup", uselist=False)
