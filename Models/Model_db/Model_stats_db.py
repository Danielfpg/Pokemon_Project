from sqlalchemy import Column, Integer, ForeignKey
from db.db_connection import Base
from sqlalchemy.orm import relationship

class StatsDB(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    carta_pokemon_id = Column(Integer, ForeignKey("cartas_Pokemon.id"), unique=True)
    speed = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    special_atk = Column(Integer, nullable=False)
    special_def = Column(Integer, nullable=False)

    carta_pokemon = relationship("CartaPokemonDB", back_populates="stats")
    carta_pokemon_backup = relationship("CartaPokemonBackupDB", back_populates="stats",uselist=False)