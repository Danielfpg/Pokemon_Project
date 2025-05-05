from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

Base = declarative_base()

class CartaPokemon(Base):
    __tablename__ = "cartas_pokemon"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_carta: Mapped[str] = mapped_column(String(50), nullable=False)
    rare: Mapped[str] = mapped_column(String(20), nullable=False)
    costo_en_bolsa: Mapped[float] = mapped_column(Float, nullable=False)

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    stats: Mapped[str] = mapped_column(String(255), nullable=False)

class CartaEntrenador(Base):
    __tablename__ = "cartas_entrenador"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_carta: Mapped[str] = mapped_column(String(50), nullable=False)
    rare: Mapped[str] = mapped_column(String(20), nullable=False)
    costo_en_bolsa: Mapped[float] = mapped_column(Float, nullable=False)

    especial: Mapped[str] = mapped_column(String(100), nullable=True)
    subtipo: Mapped[str] = mapped_column(String(50), nullable=True)
    efecto: Mapped[str] = mapped_column(String(255), nullable=True)
    tiempo: Mapped[int] = mapped_column(Integer, nullable=True)

class CartaEnergia(Base):
    __tablename__ = "cartas_energia"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_carta: Mapped[str] = mapped_column(String(50), nullable=False)
    rare: Mapped[str] = mapped_column(String(20), nullable=False)
    costo_en_bolsa: Mapped[float] = mapped_column(Float, nullable=False)

    especial: Mapped[str] = mapped_column(String(100), nullable=True)
    efecto: Mapped[str] = mapped_column(String(255), nullable=True)
    tiempo: Mapped[int] = mapped_column(Integer, nullable=True)
