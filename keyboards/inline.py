from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.button_text import ButtonText as BT
from database.models import Category, Recipe


async def categories(prefix: str, show_all_recipes=False):
    all_categories = await Category.all()
    keyboard = InlineKeyboardBuilder()
    all_recipes = await Recipe.all().count()
    if show_all_recipes:
        keyboard.add(InlineKeyboardButton(text=BT.SEARCH_ALL_RECIPES + f" ({all_recipes})", callback_data=f'{prefix}all'))
    for item in all_categories:
        category_items = await Recipe.filter(category=item).count()
        keyboard.add(InlineKeyboardButton(text=f"{item.title} ({category_items})", callback_data=f'{prefix}{item.id}'))
    return keyboard.adjust(1).as_markup()


recipe_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.PREV, callback_data='go_to_next_recipe'),
            InlineKeyboardButton(text=BT.NEXT, callback_data='go_to_prev_recipe'),
        ],
        [
            InlineKeyboardButton(text=BT.ADDED_TO_FAVOURITE_RECIPES, callback_data='add_recipe_to_favourites'),
        ],
        [
            InlineKeyboardButton(text=BT.REPORT_RECIPE, callback_data='report_recipe'),
        ]
    ]
)

my_recipe_edit_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.PREV, callback_data='go_to_next_recipe'),
            InlineKeyboardButton(text=BT.NEXT, callback_data='go_to_prev_recipe'),
        ],
        [
            InlineKeyboardButton(text=BT.CHANGE_RECIPE_NAME, callback_data='g'),
            InlineKeyboardButton(text=BT.CHANGE_RECIPE_URL, callback_data='g'),
        ],
        [
            InlineKeyboardButton(text=BT.DELETE_RECIPE, callback='g'),
        ]
    ]
)

search_type_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.SEARCH_BY_TITLE, callback_data='choose_search_type_by_name')
        ],
        [
            InlineKeyboardButton(text=BT.SEARCH_BY_AUTHOR, callback_data='choose_search_type_by_author')
        ],
        [
            InlineKeyboardButton(text=BT.SEARCH_ALL_RECIPES, callback_data='choose_search_type_by_all')
        ],
        [
            InlineKeyboardButton(text=BT.PREV, callback_data='back_to_choose_category'),
        ],
    ]
)
