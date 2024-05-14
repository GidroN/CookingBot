from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.models import User
from utils import get_main_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    tg_id = user.id
    full_name = user.first_name

    if user.last_name:
        full_name += " " + user.last_name

    username = user.username
    reply_mk = get_main_kb(str(tg_id))

    if username:
        await message.answer(f'Добро пожаловать, @{user.username}!', reply_markup=reply_mk)
    else:
        await message.answer(f'Добро пожаловать!', reply_markup=reply_mk)

    if not await User.filter(tg_id=tg_id).exists():
        await User.create(tg_id=tg_id, name=full_name.strip(), username=username)
