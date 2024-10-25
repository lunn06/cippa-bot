import logging

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot import dialogs
from bot.config import parse_config, Config
from bot.database.base import Base
from bot.middlewares.antiflood import AntiFloodMiddleware
from bot.middlewares.database import DbSessionMiddleware
from bot.storage.nats import NatsStorage
from bot.utils.nats_connection import connect_to_nats

config: Config = parse_config()

logger = logging.getLogger(__name__)
if config.debug:
    logging.basicConfig(
        level=logging.DEBUG
    )
else:
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        filemode='a',
    )


async def main():
    engine = create_async_engine(url=config.db_url.get_secret_value(), echo=config.debug)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=config.debug)

    nats_str_servers = list(map(str, config.nats_servers))
    nc, js = await connect_to_nats(
        nats_str_servers,
        config.nats_user,
        config.nats_password.get_secret_value(),
        config.nats_token.get_secret_value(),
    )
    storage = await NatsStorage.init(nc, js, key_builder=DefaultKeyBuilder(with_destiny=True))

    dp = Dispatcher(storage=storage)
    dp.message.register(dialogs.main.start_handler, CommandStart())

    dp.update.middleware(DbSessionMiddleware(session_maker))
    dp.update.middleware(AntiFloodMiddleware(config.flood_timeout))

    dp.include_routers(*dialogs.get_dialogs())

    setup_dialogs(dp)

    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == '__main__':
    uvloop.run(main(), debug=config.debug)
    # asyncio.run(main(), debug=config.debug)
