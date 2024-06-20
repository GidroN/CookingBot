from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.database.models import Recipe
from bot.database.redis_client import rc
from bot.keyboards import (admin_panel, main_menu_admin_kb,
                           main_menu_user_with_admin_option_kb, admin_manage_category_panel)
from bot.constants.button_text import ButtonText as BT
from bot.misc.filters import AdminFilter
from bot.misc.utils import (cache_list_update, convert_ids_list_into_objects,
                            send_recipe_to_check_reports, get_three_report_recipes)

router = Router(name='admin_handlers')


@router.message(AdminFilter(), F.text == BT.USER_INTERFACE)
@router.message(AdminFilter(), Command('user'))
async def change_to_user_panel(message: Message):
    await message.answer('Вы перешли в интерфейс пользователя.', reply_markup=main_menu_user_with_admin_option_kb)


@router.message(AdminFilter(), F.text == BT.ADMIN_INTERFACE)
@router.message(AdminFilter(), Command('admin'))
async def change_to_user_panel(message: Message):
    await message.answer('Вы перешли в интерфейс администратора.', reply_markup=main_menu_admin_kb)


@router.message(AdminFilter(), F.text == BT.ADMIN_PANEL)
async def show_admin_panel(message: Message):
    await message.answer('Вы перешли в панель управления.', reply_markup=admin_panel)


@router.message(AdminFilter(), F.text == BT.CHECK_REPORTS)
async def check_reports(message: Message):
    client = rc.get_client()
    key = f'{message.from_user.id}'

    recipes = await get_three_report_recipes().values_list('id', flat=True)
    recipe_ids = list(set(recipes))
    if not recipe_ids:
        await message.answer('На данный момент у вас нет активных жалоб')
        return

    cache_list_update(client, key, recipe_ids)
    recipes = await convert_ids_list_into_objects(recipe_ids, Recipe, ['category', 'creator'])
    await send_recipe_to_check_reports(recipes, message, client)


@router.message(AdminFilter(), F.text == BT.MANAGE_CATEGORIES)
async def change_category(message: Message):
    await message.answer('Выберите опцию:', reply_markup=admin_manage_category_panel)


