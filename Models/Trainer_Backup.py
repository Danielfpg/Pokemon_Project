from sqlalchemy import Column, String, Enum
from base_model import MainModel
from db.db_connection import Base
from Models.enums import TipoCartaEnum

class CartaEntrenadorBackupDB(MainModel, Base):
    __tablename__ = "cartas_entrenador_backup"
    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.entrenador, nullable=False)
    subtipo = Column(String, nullable=False)
    efecto = Column(String, nullable=False)
    tiempo = Column(String, nullable=False)
