from sqlalchemy import Column, Boolean, Enum
from base_model import MainModel
from .enums import TipoEnergiaEnum, TipoCartaEnum
from db.db_connection import Base

class CartaEnergiaBackupDB(MainModel,Base):
    __tablename__ = "cartas_energia_backup"
    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.energia, nullable=False)
    tipo = Column(Enum(TipoEnergiaEnum), nullable=False)
    especial = Column(Boolean, default=False)