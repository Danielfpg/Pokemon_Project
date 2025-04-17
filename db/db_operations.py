from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from Models.Model_Pokemon_card import CartaPokemon
from Models.Model_Energie_card import CartaEnergia
from Models.Model_Trainer_card import CartaEntrenador
# Crear carta
async def db_create_carta(
        db_session: AsyncSession,
        tipo_carta: str,
        nombre: str,
        rare: str,
        costo_en_bolsa: float,
        tipo: str = None,
        stats: str = None,
        especial: str = None,
        subtipo: str = None,
        efecto: str = None,
        tiempo: int = None
):
    if tipo_carta == "Pokemon":
        carta = CartaPokemon(
            nombre=nombre,
            tipo_carta=tipo_carta,
            rare=rare,
            costo_en_bolsa=costo_en_bolsa,
            tipo=tipo,
            stats=stats
        )
    elif tipo_carta == "Entrenador":
        carta = CartaEntrenador(
            nombre=nombre,
            tipo_carta=tipo_carta,
            rare=rare,
            costo_en_bolsa=costo_en_bolsa,
            especial=especial,
            subtipo=subtipo,
            efecto=efecto,
            tiempo=tiempo
        )
    elif tipo_carta == "Energia":
        carta = CartaEnergia(
            nombre=nombre,
            tipo_carta=tipo_carta,
            rare=rare,
            costo_en_bolsa=costo_en_bolsa,
            especial=especial,
            efecto=efecto,
            tiempo=tiempo
        )

    async with db_session.begin():
        db_session.add(carta)
        await db_session.flush()
        carta_id = carta.id
        await db_session.commit()

    return carta_id


# Obtener carta por ID
async def db_get_carta(db_session: AsyncSession, carta_id: int):
    query = select(CartaPokemon).where(CartaPokemon.id == carta_id)  # Cambiar según el tipo de carta
    result = await db_session.execute(query)
    carta = result.scalars().first()
    return carta


# Actualizar carta
async def db_update_carta(db_session: AsyncSession, carta_id: int, new_name: str):
    query = (
        update(CartaPokemon)  # Cambiar según el tipo de carta
        .where(CartaPokemon.id == carta_id)
        .values(nombre=new_name)
    )
    result = await db_session.execute(query)
    await db_session.commit()
    return result.rowcount > 0


# Eliminar carta
async def db_remove_carta(db_session: AsyncSession, carta_id: int):
    result = await db_session.execute(
        delete(CartaPokemon).where(CartaPokemon.id == carta_id)
    )
    await db_session.commit()
    return result.rowcount > 0
