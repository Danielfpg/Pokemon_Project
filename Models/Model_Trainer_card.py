from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from .base_model import MainModel
from .enums import TipoCartaEnum
from db.db_connection import Base


class CartaEntrenadorDB(MainModel,Base):
    __tablename__ = "cartas_entrenador"
    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.entrenador, nullable=False)
    subtipo=Column(String, nullable=False)
    efecto=Column(String, nullable=False)
    tiempo=Column(String, nullable=False)