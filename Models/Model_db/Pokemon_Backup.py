from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from Models.Model_db.base_model_db import MainModel
from Models.enums import TipoCartaEnum
from db.db_connection import Base

class CartaPokemonBackupDB(MainModel, Base):
    __tablename__ = "cartas_pokemon_backup"

    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.pokemon, nullable=False)
    tipo = Column(String, nullable=False)

    stats_id = Column(Integer, ForeignKey("stats.carta_pokemon_id"), nullable=True)
    stats = relationship("StatsDB", back_populates="carta_pokemon_backup", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'cartas_pokemon_backup',
    }
