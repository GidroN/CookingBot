import re
import redis
import asyncio
from typing import Any

from aiogram import Bot
from aiogram.types import Message
from redis import Redis
from tortoise import models
from tortoise.functions import Count
from tortoise.queryset import QuerySet

from keyboards.builders import user_recipe_panel, user_recipe_change_panel, \
    single_recipe_panel, admin_recipe_panel, admin_report_panel
from keyboards.reply import main_menu_user_kb, only_main_menu, main_menu_admin_kb, main_menu_user_with_admin_option_kb
from keyboards.inline import repeat_search_panel
from database.models import Recipe, Category, User, Report


async def is_admin(tg_id: int) -> bool:
    if await User.filter(tg_id=tg_id).exists():
        user = await User.get(tg_id=tg_id)
        return user.is_admin

    return False


async def notify_admins(bot: Bot, msg: str, reply_markup=None):
    admins = await User.filter(is_admin=True)
    for admin in admins:
        await bot.send_message(chat_id=admin.tg_id,
                               text=msg,
                               reply_markup=reply_markup)


async def get_main_kb(tg_id: int, only_menu: bool = False, show_admin_panel=False):
    if only_menu:
        return only_main_menu

    if await is_admin(tg_id):
        if show_admin_panel:
            return main_menu_admin_kb
        else:
            return main_menu_user_with_admin_option_kb

    return main_menu_user_kb


async def set_timer(message: Message, timer_minutes: int):
    timer_second = timer_minutes * 60
    await asyncio.sleep(timer_second)
    await message.reply('Время истекло!')


async def check_recipe_in_favourites(recipe_id: int, user_tg_id: int) -> bool:
    recipe = await Recipe.get(id=recipe_id)
    user = await User.get(tg_id=user_tg_id)
    favourite_recipes = await user.favourite_recipes.all()
    return recipe in favourite_recipes


async def send_user_recipe_info(recipes_list: list[Recipe] | list[models.Model],
                                message: Message,
                                category: Category | None = None,
                                edit_msg: bool = False,
                                print_find: bool = True,
                                page: int = 0):
    if not recipes_list:
        await message.answer('Время хранения данных истекло. Произведите новый поиск.', reply_markup=repeat_search_panel)
        return

    recipe = recipes_list[page]
    user = await User.get(tg_id=message.chat.id).prefetch_related('favourite_recipes')
    favourite = recipe in await user.favourite_recipes.filter(is_active=True)

    if print_find:
        if category:
            await message.answer(f'Найдено {len(recipes_list)} рецептов в категории {category.title}',
                                 reply_markup=await get_main_kb(message.chat.id, only_menu=True))
        else:
            await message.answer(f'Найдено {len(recipes_list)} рецептов',
                                 reply_markup=await get_main_kb(message.chat.id, only_menu=True))

    text = f"""Рецепт {page + 1}/{len(recipes_list)}
<b>{recipe.title}</b>
Категория: {recipe.category.title}
Автор: {recipe.creator.name}
{recipe.url}"""

    reply_markup = user_recipe_panel(recipe.id, favourite, page)

    if not edit_msg:
        await message.answer(text, reply_markup=reply_markup)
    else:
        await message.edit_text(text)
        await message.edit_reply_markup(reply_markup=reply_markup)


async def send_user_recipe_change(recipes_list: list[Recipe] | list[models.Model],
                                  message: Message,
                                  edit_msg: bool = False,
                                  page: int = 0):
    recipe = recipes_list[page]
    if recipe.is_active:
        msg_title = f'Рецепт {page + 1}/{len(recipes_list)}'
        reply_markup = user_recipe_change_panel(recipe.id, page)
    else:
        msg_title = f'<b>⚠ НЕ АКТИВЕН</b>\n\nРецепт {page + 1}/{len(recipes_list)}'
        reply_markup = user_recipe_change_panel(recipe.id, page, True)

    text = f"""{msg_title}
<b>{recipe.title}</b>
Категория: {recipe.category.title}
{recipe.url}"""

    if not edit_msg:
        await message.answer(text, reply_markup=reply_markup)
    else:
        await message.edit_text(text)
        await message.edit_reply_markup(reply_markup=reply_markup)


async def send_single_recipe(recipe: Recipe, message: Message):
    favourite = await check_recipe_in_favourites(recipe.id, message.chat.id)
    text = f"""<b>{recipe.title}</b>
Категория: {recipe.category.title}
Автор: {recipe.creator.name}
{recipe.url}"""
    await message.answer(text, reply_markup=single_recipe_panel(recipe.id, favourite))


async def send_recipe_to_check_reports(recipes_list: list[Recipe] | list[models.Model],
                                       message: Message,
                                       client: Redis,
                                       edit_msg: bool = False,
                                       page: int = 0):
    recipe = recipes_list[page]
    text = f"""Рецепт {page + 1}/{len(recipes_list)}
<b>{recipe.title}</b>
id рецепта: {recipe.id}
Категория: {recipe.category.title}
Автор: {recipe.creator.name}
id автора: {recipe.creator.tg_id}
{recipe.url}"""

    reply_markup = await admin_recipe_panel(recipe.id, page)

    if edit_msg:
        await message.edit_text(text)
        await message.edit_reply_markup(reply_markup=reply_markup)
    else:
        await message.answer(text, reply_markup=reply_markup)


async def send_report_reason(reports_list: list[Report] | list[models.Model],
                             message: Message,
                             edit_msg: bool = False,
                             page: int = 0):
    report = reports_list[page]
    text = f"""Причина жалобы {page + 1}/{len(reports_list)}
Пользователь: {report.user.name}

<b>Причина:</b>
<i>{report.reason}</i>"""

    reply_markup = await admin_report_panel(page)

    if edit_msg:
        await message.edit_text(text)
        await message.edit_reply_markup(reply_markup=reply_markup)
    else:
        await message.answer(text, reply_markup=reply_markup)


def get_list_from_cache(client: redis.Redis, key: str, types: Any) -> list:
    if issubclass(types, int):
        lst = [int(item) for item in client.lrange(key, 0, -1)]
    else:
        lst = [item.decode() for item in client.lrange(key, 0, -1)]
    lst.reverse()
    return lst


async def convert_ids_list_into_objects(ids_list: list[int], model: models.Model, prefetch_related: list = None) -> list[models.Model]:
    prefetch_related = [] if not prefetch_related else prefetch_related
    return await model.filter(id__in=ids_list).prefetch_related(*prefetch_related)


def cache_list_update(client: redis.Redis, key: str, lst: list) -> None:
    client.delete(key)
    client.lpush(key, *lst)
    client.expire(key, 60 * 15)


def get_popular_recipes() -> QuerySet[models.MODEL]:
    recipes = Recipe.annotate(
        favourite_count=Count('recipe_favourites')
    ).order_by('-favourite_count', 'title').filter(is_active=True)

    return recipes


def get_three_report_recipes() -> QuerySet[models.MODEL]:
    recipes = Recipe.annotate(
        report_count=Count('recipe_report')
    ).filter(report_count__gte=3)

    return recipes
