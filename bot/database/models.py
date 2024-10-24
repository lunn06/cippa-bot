from typing import Optional

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import Base


class User(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True
    )
    user_name: Mapped[Optional[str]] = mapped_column(
        nullable=True
    )
    registered_at: Mapped[int] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )
