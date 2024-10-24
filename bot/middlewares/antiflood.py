import datetime
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import LRUCache


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_delta: float):
        self.cache = LRUCache(maxsize=512)
        self.timedelta_limiter: datetime.timedelta = datetime.timedelta(seconds=time_delta)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        user = data.get('event_from_user')
        assert isinstance(user, User)

        last_message_time: datetime.datetime = self.cache.get(user.id)
        now = datetime.datetime.now()
        if last_message_time is None:
            self.cache[user.id] = now
            return await handler(event, data)

        self.cache[user.id] = now
        if now - last_message_time > self.timedelta_limiter:
            return await handler(event, data)
