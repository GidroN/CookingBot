from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from database.redis_client import rc
from keyboards import main_menu_user_with_admin_option_kb, main_menu_admin_kb, admin_panel
from keyboards.button_text import ButtonText as BT
from database.models import Recipe, Report
from misc.filters import AdminFilter
from misc.utils import send_single_recipe, convert_ids_list_into_objects, cache_list_update, \
    send_recipe_to_check_reports

router = Router(name='admin_handlers')


@router.message(AdminFilter(), Command('get_recipe_by_id'))
async def get_recipe_by_id(message: Message):
    recipe_id = message.text.split()[-1]
    recipe = await Recipe.get_or_none(id=recipe_id).prefetch_related('creator', 'category')
    if recipe:
        await send_single_recipe(recipe, message, True)
    else:
        await message.answer('По этому id ничего не найдено.')


@router.message(AdminFilter(), F.text == BT.USER_INTERFACE)
async def change_to_user_panel(message: Message):
    await message.answer('Вы перешли в интерфейс пользователя.', reply_markup=main_menu_user_with_admin_option_kb)


@router.message(AdminFilter(), F.text == BT.ADMIN_INTERFACE)
async def change_to_user_panel(message: Message):
    await message.answer('Вы перешли в интерфейс администратора.', reply_markup=main_menu_admin_kb)


@router.message(AdminFilter(), F.text == BT.ADMIN_PANEL)
async def show_admin_panel(message: Message):
    await message.answer('Вы перешли в панель управления.', reply_markup=admin_panel)


@router.message(AdminFilter(), F.text == BT.CHECK_REPORTS)
async def check_reports(message: Message):
    client = rc.get_client()
    key = f'{message.from_user.id}'
    recipe_ids = list(set(await Report.all().values_list('recipe__id', flat=True)))
    cache_list_update(client, key, recipe_ids)
    recipes = await convert_ids_list_into_objects(recipe_ids, Recipe, ['category', 'creator'])
    await send_recipe_to_check_reports(recipes, message, client)
