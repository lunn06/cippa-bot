import logging

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import parse_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():
    config = parse_config()

    # engine = create_async_engine(url=config.db_url.get_secret_value(), echo=config.debug)

    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()

    await dp.start_polling(bot)


if __name__ == '__main__':
    uvloop.run(main())
