import logging
import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from tortoise import Tortoise
from redis.exceptions import ConnectionError

from database.connection import init
from misc.routers import router
from misc.config import BOT_TOKEN, REDIS_HOST, REDIS_PORT
from misc.middlewares import CheckUserExistsMiddleware
from database.redis_client import rc


async def main():
    # set up logging config
    logging.basicConfig(level=logging.INFO)

    # init db and redis
    await init(generate_schemas=False)
    rc.connect(host=REDIS_HOST, port=REDIS_PORT)

    # set up bot
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=BOT_TOKEN, default=default)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    dp.message.middleware(CheckUserExistsMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, close_bot_session=False)
    finally:
        # shutdown bot
        tasks = [dp.storage.close(), Tortoise.close_connections()]
        await asyncio.wait([asyncio.create_task(task) for task in tasks])
        rc.disconnect()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Bot stopped successfully.')
    except (TelegramNetworkError, ConnectionError, SystemExit):
        logging.warning('Bot stopped during and error.')
        exit(1)
