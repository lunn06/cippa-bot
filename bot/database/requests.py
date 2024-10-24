from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User, UserFullName, UserCity, UserPreschool, UserPosition


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == user_id)

    return await session.scalar(stmt)


async def ensure_user(session: AsyncSession, user_id: int, user_name: str | None) -> None:
    existing = await get_user_by_id(session, user_id)
    if existing is not None:
        return None

    user = User(telegram_id=user_id, telegram_name=user_name)
    session.add(user)

    await session.commit()


async def ensure_user_fullname(session: AsyncSession, user_id: int, full_name: str) -> None:
    stmt = select(
        UserFullName
    ).where(
        and_(
            UserFullName.telegram_id == user_id,
            UserFullName.full_name == full_name,
        )
    )
    existing = await session.scalar(stmt)
    if existing is not None:
        return

    user_full_name = UserFullName(telegram_id=user_id, full_name=full_name)
    session.add(user_full_name)

    await session.commit()


async def ensure_user_city(session: AsyncSession, user_id: int, city: str) -> None:
    stmt = select(
        UserCity
    ).where(
        and_(
            UserCity.telegram_id == user_id,
            UserCity.city == city,
        )
    )
    existing = await session.scalar(stmt)
    if existing is not None:
        return

    user_city = UserCity(telegram_id=user_id, city=city)
    session.add(user_city)

    await session.commit()


async def ensure_user_preschool(session: AsyncSession, user_id: int, preschool: str) -> None:
    stmt = select(
        UserPreschool
    ).where(
        and_(
            UserPreschool.telegram_id == user_id,
            UserPreschool.preschool == preschool,
        )
    )
    existing = await session.scalar(stmt)
    if existing is not None:
        return

    user_preschool = UserPreschool(telegram_id=user_id, preschool=preschool)
    session.add(user_preschool)

    await session.commit()


async def ensure_user_position(session: AsyncSession, user_id: int, position: str) -> None:
    stmt = select(
        UserPosition
    ).where(
        and_(
            UserPosition.telegram_id == user_id,
            UserPosition.position == position,
        )
    )
    existing = await session.scalar(stmt)
    if existing is not None:
        return

    user_position = UserPosition(telegram_id=user_id, position=position)
    session.add(user_position)

    await session.commit()
