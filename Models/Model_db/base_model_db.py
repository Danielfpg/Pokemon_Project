from sqlalchemy import Column, Integer, String, Float, Enum
from db.db_connection import Base
from Models.enums import RarezaEnum


class MainModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    nombre = Column(String(50), nullable=False, unique=True, index=True)  # Nombre único y con índice
    rare = Column(Enum(RarezaEnum), nullable=False)
    costo_en_bolsa = Column(Float, nullable=False)


    __mapper_args__ = {
        'polymorphic_on': rare
    }