from sqlalchemy import Column, Integer, ForeignKey
from db.db_connection import Base
from sqlalchemy.orm import relationship

class StatsDB(Base):
    __tablename__ = "stats"
    carta_pokemon_id = Column(Integer, ForeignKey("cartas_pokemon.id"), primary_key=True)
    speed = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    special_atk = Column(Integer, nullable=False)
    special_def = Column(Integer, nullable=False)

    carta_pokemon = relationship("CartaPokemonDB", back_populates="stats")