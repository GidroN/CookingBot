from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.factories import RecipePaginationCallback, PaginationAction, AddRecipeToFavouritesCallback, \
    ReportRecipeCallback
from keyboards.button_text import ButtonText as BT
from database.models import Category, Recipe


async def categories(prefix: str, show_all_recipes=False):
    all_categories = await Category.all()
    all_recipes = await Recipe.all().count()
    keyboard = InlineKeyboardBuilder()
    if show_all_recipes:
        keyboard.add(InlineKeyboardButton(text=BT.SEARCH_ALL_RECIPES + f" ({all_recipes})", callback_data=f'{prefix}all'))
    for item in all_categories:
        category_items = await Recipe.filter(category=item).count()
        keyboard.add(InlineKeyboardButton(text=f"{item.title} ({category_items})", callback_data=f'{prefix}{item.id}'))
    return keyboard.adjust(1).as_markup()


def user_recipe_panel(recipe_id: int, favourite: bool = False, page: int = 0):
    keyboard = InlineKeyboardBuilder()
    favourite_recipe = BT.ADDED_TO_FAVOURITE_RECIPES if favourite else BT.ADD_TO_FAVOURITE_RECIPES
    keyboard.add(
        InlineKeyboardButton(text=BT.PREV, callback_data=RecipePaginationCallback(page=page,
                                                                                  action=PaginationAction.prev).pack()),
        InlineKeyboardButton(text=BT.NEXT, callback_data=RecipePaginationCallback(page=page,
                                                                                  action=PaginationAction.next).pack()),
        InlineKeyboardButton(text=favourite_recipe, callback_data=AddRecipeToFavouritesCallback(page=page,
                                                                                                recipe_id=recipe_id).pack()),
        InlineKeyboardButton(text=BT.REPORT_RECIPE, callback_data=ReportRecipeCallback(recipe_id=recipe_id).pack()),
    )
    return keyboard.adjust(2, 1, 1).as_markup()


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
            InlineKeyboardButton(text=BT.DELETE_RECIPE, callback_data='g'),
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
