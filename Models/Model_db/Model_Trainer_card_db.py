from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from Models.Model_db.base_model_db import MainModel
from Models.enums import TipoCartaEnum
from db.db_connection import Base


class CartaEntrenadorDB(MainModel, Base):
    __tablename__ = "cartas_entrenador"

    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.entrenador, nullable=False)
    subtipo = Column(String, nullable=False)
    efecto = Column(String, nullable=False)
    tiempo = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'cartas_entrenador',
    }
