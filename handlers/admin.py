from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from database.models import Recipe
from filters import AdminFilter

router = Router(name='admin_handlers')


@router.message(AdminFilter(), Command('get_recipe_by_id'))
async def get_recipe_by_id(message: Message):
    recipe_id = message.text.split()[-1]
    recipe = Recipe.get(id=recipe_id)
    await message.answer('RECIPE')
