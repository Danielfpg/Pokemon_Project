from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

# Modelo base para las cartas
class CartaBase(Base):
    __tablename__ = "cartas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_carta: Mapped[str] = mapped_column(String(50), nullable=False)
    rare: Mapped[str] = mapped_column(String(20), nullable=False)
    costo_en_bolsa: Mapped[float] = mapped_column(Float, nullable=False)

# Modelo para la carta de Pokémon
class CartaPokemon(CartaBase):
    __tablename__ = "cartas_pokemon"
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    stats: Mapped[str] = mapped_column(String(255), nullable=False)  # Para los stats específicos de Pokémon

# Modelo para la carta de Entrenador
class CartaEntrenador(CartaBase):
    __tablename__ = "cartas_entrenador"
    especial: Mapped[str] = mapped_column(String(100), nullable=True)
    subtipo: Mapped[str] = mapped_column(String(50), nullable=True)
    efecto: Mapped[str] = mapped_column(String(255), nullable=True)
    tiempo: Mapped[int] = mapped_column(Integer, nullable=True)

# Modelo para la carta de Energía
class CartaEnergia(CartaBase):
    __tablename__ = "cartas_energia"
    especial: Mapped[str] = mapped_column(String(100), nullable=True)
    efecto: Mapped[str] = mapped_column(String(255), nullable=True)
    tiempo: Mapped[int] = mapped_column(Integer, nullable=True)
