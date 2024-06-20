from aiogram.filters import Filter
from aiogram.types import Message

from bot.database.models import User
from bot.misc.utils import is_admin


class AdminFilter(Filter):

    async def __call__(self, message: Message):
        return await is_admin(message.from_user.id)


class IsNotActiveUser(Filter):
    async def __call__(self, message: Message):
        if await User.filter(tg_id=message.from_user.id).exists():
            user = await User.get(tg_id=message.from_user.id)
            return not user.is_active
        return False
