from sqlalchemy import Column, Integer, Boolean, Enum, ForeignKey
from Models.Model_db.base_model_db import MainModel
from Models.enums import TipoEnergiaEnum, TipoCartaEnum
from db.db_connection import Base


class CartaEnergiaBackupDB(MainModel, Base):
    __tablename__ = "cartas_energia_backup"

    tipo_carta = Column(Enum(TipoCartaEnum), default=TipoCartaEnum.energia, nullable=False)
    tipo = Column(Enum(TipoEnergiaEnum), nullable=False)
    especial = Column(Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'cartas_energia_backup',
    }
