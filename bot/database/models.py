from typing import Optional

from sqlalchemy import TIMESTAMP, func, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import Base


class User(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True
    )
    telegram_name: Mapped[Optional[str]] = mapped_column(
        VARCHAR(32),
        nullable=True
    )
    registered_at: Mapped[int] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )


class UserFullName(Base):
    __tablename__ = "users_names"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(User.telegram_id),
        primary_key=True,
    )
    full_name: Mapped[str] = mapped_column(
        VARCHAR(100),
        primary_key=True,
    )


class UserCity(Base):
    __tablename__ = "users_cities"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(User.telegram_id),
        primary_key=True,
    )
    city: Mapped[str] = mapped_column(
        VARCHAR(32),
        primary_key=True,
    )


class UserPreschool(Base):
    __tablename__ = "users_preschools"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(User.telegram_id),
        primary_key=True,
    )
    preschool: Mapped[str] = mapped_column(
        VARCHAR(32),
        primary_key=True,
    )


class UserPosition(Base):
    __tablename__ = "users_positions"
    telegram_id: Mapped[int] = mapped_column(
        ForeignKey(User.telegram_id),
        primary_key=True,
    )
    position: Mapped[str] = mapped_column(
        VARCHAR(32),
        primary_key=True,
    )
