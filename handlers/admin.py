from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import main_menu_user_with_admin_option_kb, main_menu_admin_kb
from keyboards.button_text import ButtonText as BT
from database.models import Recipe
from misc.filters import AdminFilter
from misc.utils import send_single_recipe

router = Router(name='admin_handlers')


@router.message(AdminFilter(), Command('get_recipe_by_id'))
# @Router.message(AdminFilter(), ...)
async def get_recipe_by_id(message: Message):
    recipe_id = message.text.split()[-1]
    recipe = await Recipe.get_or_none(id=recipe_id).prefetch_related('creator', 'category')
    if recipe:
        await send_single_recipe(recipe, message, True)
    else:
        await message.answer('По этому id ничего не найдено.')


@router.message(AdminFilter(), Command('go_to_user_panel'))
@router.message(AdminFilter(), F.text == BT.USER_PANEL)
async def change_to_user_panel(message: Message):
    await message.answer('Вы перешли в интерфейс пользователя.', reply_markup=main_menu_user_with_admin_option_kb)


@router.message(AdminFilter(), Command('go_to_admin_panel'))
@router.message(AdminFilter(), F.text == BT.ADMIN_PANEL)
async def change_to_user_panel(message: Message):
    await message.answer('Вы перешли в интерфейс пользователя.', reply_markup=main_menu_admin_kb)


