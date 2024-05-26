from aiogram.filters import Filter
from aiogram.types import Message
from misc.config import ADMINS


class AdminFilter(Filter):

    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins
