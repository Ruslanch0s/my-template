import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from config import BOT_TOKEN
from handlers.echo.echo import register_echo
from handlers.deeplink.deeplink import register_deeplink
from middlewares.antiflood import ThrottlingMiddleware
from utils.notify_admins import on_startup_notify
from utils.logging import logging


def register_all_middlewares(dp):
    # dp.setup_middleware(DbMiddleware())
    dp.setup_middleware(ThrottlingMiddleware())


def register_all_filters(dp):
    # dp.filters_factory.bind(AdminFilter)
    pass


def register_all_handlers(dp):
    register_deeplink(dp)
    register_echo(dp)


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)  # + html стили для текста
    # Throttling manager does not work without storage
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
    await dp.skip_updates()  # Пропустить полученые обновления

    register_all_middlewares(dp)
    register_all_handlers(dp)

    await on_startup_notify(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")

