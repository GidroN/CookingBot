from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Category, Recipe
from keyboards import BackToType, ChooseSearchTypeCallback, SearchType, ChooseSearchTypeAction
from keyboards.factories import RecipePaginationCallback, PaginationAction, PaginationMarkup, \
    AddRecipeToFavouritesCallback, \
    ReportRecipeCallback, ChangeRecipeInfoCallback, RecipeChangeItem, BackCallback, ChooseSearchTypeByCategoryCallback
from keyboards.button_text import ButtonText as BT


async def categories(prefix: str):
    all_categories = await Category.all()
    keyboard = InlineKeyboardBuilder()
    for item in all_categories:
        category_items = await Recipe.filter(category=item).count()
        keyboard.add(InlineKeyboardButton(text=f"{item.title} ({category_items})", callback_data=f'{prefix}{item.id}'))
    keyboard.adjust(2)
    keyboard.row(
        InlineKeyboardButton(text=BT.PREV, callback_data=BackCallback(back_to_type=BackToType.CHOOSE_SEARCH_TYPE,
                                                                      change_kb=False).pack())
    )
    return keyboard.as_markup()


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
                                                                         recipe_id=recipe_id,
                                                                         single_recipe_view=False).pack()),
        InlineKeyboardButton(text=BT.REPORT_RECIPE,
                             callback_data=ReportRecipeCallback(recipe_id=recipe_id).pack()),
        InlineKeyboardButton(text=BT.SEARCH_REPEAT,
                             callback_data=BackCallback(back_to_type=BackToType.CHOOSE_SEARCH_TYPE,
                                                        change_kb=False).pack())
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


def single_recipe_panel(recipe_id: int, favourite: bool):
    keyboard = InlineKeyboardBuilder()
    favourite_recipe = BT.ADDED_TO_FAVOURITE_RECIPES if favourite else BT.ADD_TO_FAVOURITE_RECIPES
    keyboard.add(
        InlineKeyboardButton(text=favourite_recipe,
                             callback_data=AddRecipeToFavouritesCallback(page=0,
                                                                         recipe_id=recipe_id,
                                                                         single_recipe_view=True).pack()),
        InlineKeyboardButton(text=BT.REPORT_RECIPE,
                             callback_data=ReportRecipeCallback(recipe_id=recipe_id).pack()),
    )

    return keyboard.adjust(1).as_markup()


def single_recipe_change_panel(recipe_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
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

    return keyboard.adjust(2, 1).as_markup()


async def search_type_panel():
    keyboard = InlineKeyboardBuilder()
    all_categories = await Category.all().count()
    all_recipes = await Recipe.all().count()

    keyboard.add(
        InlineKeyboardButton(text=BT.SEARCH_POPULAR,
                             callback_data=ChooseSearchTypeCallback(type=SearchType.POPULAR).pack()),
        InlineKeyboardButton(text=f'{BT.SEARCH_ALL_RECIPES} ({all_recipes})',
                             callback_data=ChooseSearchTypeCallback(type=SearchType.ALL_RECIPES).pack()),
        InlineKeyboardButton(text=f'{BT.SEARCH_BY_CATEGORY} ({all_categories})',
                             callback_data=ChooseSearchTypeCallback(type=SearchType.BY_CATEGORY).pack())
    )

    return keyboard.adjust(1).as_markup()


def search_by_category_panel(back_to: str):
    # TODO: make a factory for callbacks

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=BT.SEARCH_BY_TITLE,
                             callback_data=ChooseSearchTypeByCategoryCallback(
                                 search_type=ChooseSearchTypeAction.SEARCH_BY_TITLE).pack()),
        InlineKeyboardButton(text=BT.SEARCH_BY_AUTHOR,
                             callback_data=ChooseSearchTypeByCategoryCallback(
                                 search_type=ChooseSearchTypeAction.SEARCH_BY_AUTHOR).pack()),
        InlineKeyboardButton(text=BT.SEARCH_ALL_RECIPES,
                             callback_data=ChooseSearchTypeByCategoryCallback(
                                 search_type=ChooseSearchTypeAction.SEARCH_ALL).pack()),
    )

    if back_to == 'choose_search_type':
        callback_data = BackCallback(back_to_type=BackToType.CHOOSE_SEARCH_TYPE, change_kb=False).pack()
    else:
        callback_data = BackCallback(back_to_type=BackToType.CHOOSE_CATEGORY, change_kb=False).pack()

    keyboard.add(
        InlineKeyboardButton(text=BT.PREV, callback_data=callback_data)
    )

    return keyboard.adjust(1).as_markup()
