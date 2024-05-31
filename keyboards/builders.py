from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Category, Recipe
from keyboards.factories import RecipePaginationCallback, PaginationAction, PaginationMarkup, AddRecipeToFavouritesCallback, \
    ReportRecipeCallback, ChangeRecipeInfoCallback, RecipeChangeItem
from keyboards.button_text import ButtonText as BT


async def categories(prefix: str, show_all_recipes=False):
    all_categories = await Category.all()
    all_recipes = await Recipe.all().count()
    keyboard = InlineKeyboardBuilder()
    if show_all_recipes:
        keyboard.add(
            InlineKeyboardButton(text=BT.SEARCH_ALL_RECIPES + f" ({all_recipes})", callback_data=f'{prefix}all'))
    for item in all_categories:
        category_items = await Recipe.filter(category=item).count()
        keyboard.add(InlineKeyboardButton(text=f"{item.title} ({category_items})", callback_data=f'{prefix}{item.id}'))
    return keyboard.adjust(2).as_markup()


def user_recipe_panel(recipe_id: int, favourite: bool = False, page: int = 0):
    keyboard = InlineKeyboardBuilder()
    favourite_recipe = BT.ADDED_TO_FAVOURITE_RECIPES if favourite else BT.ADD_TO_FAVOURITE_RECIPES
    keyboard.add(
        InlineKeyboardButton(text=BT.PREV,
                             callback_data=RecipePaginationCallback(page=page,
                                                                    action=PaginationAction.PREV,
                                                                    markup=PaginationMarkup.VIEWER).pack()),
        InlineKeyboardButton(text=BT.NEXT,
                             callback_data=RecipePaginationCallback(page=page,
                                                                    action=PaginationAction.NEXT,
                                                                    markup=PaginationMarkup.VIEWER).pack()),
        InlineKeyboardButton(text=favourite_recipe,
                             callback_data=AddRecipeToFavouritesCallback(page=page,
                                                                         recipe_id=recipe_id).pack()),
        InlineKeyboardButton(text=BT.REPORT_RECIPE,
                             callback_data=ReportRecipeCallback(recipe_id=recipe_id).pack()),
    )
    return keyboard.adjust(2, 1, 1).as_markup()


def user_recipe_change_panel(recipe_id: int, page: int = 0):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(

        InlineKeyboardButton(text=BT.PREV,
                             callback_data=RecipePaginationCallback(page=page,
                                                                    action=PaginationAction.PREV,
                                                                    markup=PaginationMarkup.OWNER).pack()),
        InlineKeyboardButton(text=BT.NEXT,
                             callback_data=RecipePaginationCallback(page=page,
                                                                    action=PaginationAction.NEXT,
                                                                    markup=PaginationMarkup.OWNER).pack()),
        InlineKeyboardButton(text=BT.CHANGE_RECIPE_NAME,
                             callback_data=ChangeRecipeInfoCallback(recipe_id=recipe_id,
                                                                    change_item=RecipeChangeItem.NAME, ).pack()),
        InlineKeyboardButton(text=BT.CHANGE_RECIPE_URL,
                             callback_data=ChangeRecipeInfoCallback(recipe_id=recipe_id,
                                                                    change_item=RecipeChangeItem.LINK).pack()),
        InlineKeyboardButton(text=BT.CHANGE_RECIPE_CATEGORY,
                             callback_data=ChangeRecipeInfoCallback(recipe_id=recipe_id,
                                                                    change_item=RecipeChangeItem.CATEGORY).pack()),
        InlineKeyboardButton(text=BT.DELETE_RECIPE,
                             callback_data=ChangeRecipeInfoCallback(recipe_id=recipe_id,
                                                                    change_item=RecipeChangeItem.DELETE).pack()),
    )

    return keyboard.adjust(2, 2, 1, 1).as_markup()
