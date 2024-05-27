import re
import redis
import asyncio
from typing import Any

from aiogram.types import Message
from tortoise import models

from keyboards import user_recipe_panel
from keyboards.reply import main_menu_user_kb, only_main_menu
from misc.config import ADMINS
from database.models import Recipe, Category, User


def is_admin(tg_id: str) -> bool:
    return tg_id in ADMINS


def get_main_kb(tg_id: int, only_menu=False):
    if only_menu:
        return only_main_menu

    return main_menu_user_kb


def extract_recipe_info(text):
    lines = text.strip().split('\n')

    name_line = lines[0].strip()
    url_line = lines[1].strip()

    name_match = re.match(r"^\d+\)\s*(.+)", name_line)
    name = name_match.group(1) if name_match else None

    url_match = re.match(r"^\d+\)\s*(https?://[^\s]+)", url_line)
    url = url_match.group(1) if url_match else None

    return name, url


async def set_timer(message: Message, timer_minutes: int):
    timer_second = timer_minutes * 60
    await asyncio.sleep(timer_second)
    await message.reply('Время истекло!')


async def send_user_recipe_info(recipes_list: list[Recipe],
                                message: Message,
                                category: Category | None = None,
                                edit_msg: bool = False,
                                print_find: bool = True,
                                page: int = 0):
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


async def send_user_recipe_change(recipes_list: list[Recipe],
                                  message: Message,
                                  edit_msg: bool = False,
                                  page: int = 0):
    recipe = recipes_list[page]
    user = await User.get(tg_id=message.chat.id)

    text = f"""Рецепт {page + 1}/{len(recipes_list)}
<b>{recipe.title}</b>
Категория: {recipe.category.title}
{recipe.url}"""

    reply_markup = ...
    if not edit_msg:
        await message.answer(text, reply_markup=reply_markup)
    else:
        await message.edit_text(text)
        await message.edit_reply_markup(reply_markup=reply_markup)


def get_ids_list_from_cache(client: redis.Redis, key: str, types: Any) -> list:
    if issubclass(types, int):
        lst = [int(item) for item in client.lrange(key, 0, -1)]
    else:
        lst = [item.decode() for item in client.lrange(key, 0, -1)]
    lst.reverse()
    return lst


async def convert_ids_list_into_objects(ids_list: list[int], model: models.Model, prefetch_related: list = None) -> list[models.Model]:
    prefetch_related = [] if not prefetch_related else prefetch_related
    return await model.filter(id__in=ids_list).prefetch_related(*prefetch_related)
