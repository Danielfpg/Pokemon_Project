from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from Models.Model_db.base_model_db import MainModel
from Models.enums import TipoCartaEnum
from db.db_connection import Base
from sqlalchemy.orm import validates

class CartaPokemonDB(MainModel, Base):
    __tablename__ = "cartas_Pokemon"

    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.pokemon, nullable=False)
    tipo = Column(String, nullable=False)
    stats = relationship("StatsDB", back_populates="carta_pokemon", uselist=False,lazy="selectin",cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'cartas_Pokemon',
    }

    # Validación del nombre
    @validates('nombre')
    def validate_nombre(self, key, value):
        if len(value) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return value
from Models.Model_db.Model_stats_db import StatsDB