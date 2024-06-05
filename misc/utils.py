import re
import redis
import asyncio
from typing import Any

from aiogram.types import Message
from tortoise import models
from tortoise.expressions import Q
from tortoise.functions import Count

from keyboards.builders import single_recipe_change_panel, user_recipe_panel, user_recipe_change_panel, single_recipe_panel
from keyboards.reply import main_menu_user_kb, only_main_menu, main_menu_admin_kb, main_menu_user_with_admin_option_kb
from keyboards.inline import repeat_search_panel
from misc.config import ADMINS
from database.models import Recipe, Category, User


def is_admin(tg_id: int) -> bool:
    return tg_id in ADMINS


def get_main_kb(tg_id: int, only_menu: bool = False, show_admin_panel=False):
    if only_menu:
        return only_main_menu

    if is_admin(tg_id):
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
    favourite = recipe in await user.favourite_recipes.all()

    if print_find:
        if category:
            await message.answer(f'Найдено {len(recipes_list)} рецептов в категории {category.title}',
                                 reply_markup=get_main_kb(message.chat.id, only_menu=True))
        else:
            await message.answer(f'Найдено {len(recipes_list)} рецептов',
                                 reply_markup=get_main_kb(message.chat.id, only_menu=True))

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
    text = f"""Рецепт {page + 1}/{len(recipes_list)}
<b>{recipe.title}</b>
Категория: {recipe.category.title}
{recipe.url}"""

    reply_markup = user_recipe_change_panel(recipe.id, page)
    if not edit_msg:
        await message.answer(text, reply_markup=reply_markup)
    else:
        await message.edit_text(text)
        await message.edit_reply_markup(reply_markup=reply_markup)


async def send_single_recipe(recipe: Recipe, message: Message, edit: bool = False):
    favourite = await check_recipe_in_favourites(recipe.id, message.chat.id)
    text = f"""<b>{recipe.title}</b>
Категория: {recipe.category.title}
Автор: {recipe.creator.name}
{recipe.url}"""
    if edit:
        await message.answer(text, reply_markup=single_recipe_change_panel(recipe.id))
    else:
        await message.answer(text, reply_markup=single_recipe_panel(recipe.id, favourite))


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


async def get_popular_recipes() -> list[Recipe]:
    recipes = await Recipe.annotate(
        favourite_count=Count('recipe_favourites')
    ).order_by('-favourite_count', 'title').all()

    return recipes
