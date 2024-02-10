from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject

from dotenv import load_dotenv
import asyncio
import random
import os

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode='HTML')
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Hello, <b>@{message.from_user.username}</b>')


@dp.message(Command(commands=['rn', 'random-number']))
async def get_random_number(message: Message, command: CommandObject):
    args = command.args
    if args:
        a, b = [int(n) for n in args.split('-')]
        num = random.randint(a, b)
        await message.reply(f'Your random number: {num}')
    else:
        await message.reply(f'Need arguments!')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())