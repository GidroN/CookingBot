import logging
import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from tortoise import Tortoise

from database.connection import init
from misc.routers import router
from misc.config import BOT_TOKEN, REDIS_HOST, REDIS_PORT
from database.redis_client import rc


async def main():
    # set up logging config
    logging.basicConfig(level=logging.INFO)

    # init db and redis
    await init()
    client = rc.connect(host=REDIS_HOST, port=REDIS_PORT)

    # other things
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=BOT_TOKEN, default=default)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, close_bot_session=False)
    finally:
        # shutdown bot
        tasks = [dp.storage.close(), Tortoise.close_connections()]
        await asyncio.wait([asyncio.create_task(task) for task in tasks])
        client.disconnect()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped successfully.')
