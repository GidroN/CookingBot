from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Category, Recipe, Report
from keyboards import BackToType, ChooseSearchTypeCallback, SearchType, ChooseSearchTypeAction, PaginationKey, \
    UserChangeItem
from keyboards.callback_constants import CallbackConstants
from keyboards.factories import PaginationCallback, PaginationAction, PaginationMarkup, \
    AddRecipeToFavouritesCallback, \
    ReportRecipeCallback, ChangeRecipeInfoCallback, RecipeChangeItem, BackCallback, ChooseSearchTypeByCategoryCallback, \
    CheckReportsCallback, FalseAlarmRecipeCallback, WarnUserCallback, ChangeUserInfoCallback
from keyboards.button_text import ButtonText as BT


async def categories(prefix: str, prev: bool = True, cancel: bool = False):
    all_categories = await Category.all()
    keyboard = InlineKeyboardBuilder()
    for item in all_categories:
        category_items = await Recipe.filter(category=item).count()
        keyboard.add(InlineKeyboardButton(text=f"{item.title} ({category_items})", callback_data=f'{prefix}{item.id}'))
    keyboard.adjust(2)
    if prev:
        keyboard.row(
            InlineKeyboardButton(text=BT.PREV, callback_data=BackCallback(back_to_type=BackToType.CHOOSE_SEARCH_TYPE,
                                                                          change_kb=False).pack())
        )
    if cancel:
        keyboard.row(
            InlineKeyboardButton(text=BT.CANCEL, callback_data=f'{prefix}delete')
        )
    return keyboard.as_markup()


def user_recipe_panel(recipe_id: int, favourite: bool = False, page: int = 0):
    keyboard = InlineKeyboardBuilder()
    favourite_recipe = BT.ADDED_TO_FAVOURITE_RECIPES if favourite else BT.ADD_TO_FAVOURITE_RECIPES
    keyboard.add(
        InlineKeyboardButton(text=BT.PREV,
                             callback_data=PaginationCallback(page=page,
                                                              action=PaginationAction.PREV,
                                                              markup=PaginationMarkup.VIEWER,
                                                              key=PaginationKey.DEFAULT).pack()),
        InlineKeyboardButton(text=BT.NEXT,
                             callback_data=PaginationCallback(page=page,
                                                              action=PaginationAction.NEXT,
                                                              markup=PaginationMarkup.VIEWER,
                                                              key=PaginationKey.DEFAULT).pack()),
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
                             callback_data=PaginationCallback(page=page,
                                                              action=PaginationAction.PREV,
                                                              markup=PaginationMarkup.OWNER,
                                                              key=PaginationKey.DEFAULT).pack()),
        InlineKeyboardButton(text=BT.NEXT,
                             callback_data=PaginationCallback(page=page,
                                                              action=PaginationAction.NEXT,
                                                              markup=PaginationMarkup.OWNER,
                                                              key=PaginationKey.DEFAULT).pack()),
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


async def admin_recipe_panel(recipe_id: int, page: int):
    keyboard = InlineKeyboardBuilder()
    reports_count = await Report.filter(recipe__id=recipe_id).count()
    keyboard.row(
        InlineKeyboardButton(text=BT.PREV, callback_data=PaginationCallback(action=PaginationAction.PREV,
                                                                            markup=PaginationMarkup.ADMIN_RECIPE,
                                                                            page=page,
                                                                            key=PaginationKey.DEFAULT).pack()),
        InlineKeyboardButton(text=BT.NEXT, callback_data=PaginationCallback(action=PaginationAction.NEXT,
                                                                            markup=PaginationMarkup.ADMIN_RECIPE,
                                                                            page=page,
                                                                            key=PaginationKey.DEFAULT).pack()),
    )
    keyboard.add(
        InlineKeyboardButton(text=BT.FALSE_ALARM, callback_data=FalseAlarmRecipeCallback(recipe_id=recipe_id).pack()),
        InlineKeyboardButton(text=BT.WARN_USER, callback_data=WarnUserCallback(recipe_id=recipe_id).pack()),
        InlineKeyboardButton(text=f'{BT.CHECK_REPORTS} ({reports_count})',
                             callback_data=CheckReportsCallback(recipe_id=recipe_id).pack())
    )

    return keyboard.adjust(2, 1).as_markup()


async def admin_report_panel(page: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=BT.PREV, callback_data=PaginationCallback(action=PaginationAction.PREV,
                                                                            markup=PaginationMarkup.ADMIN_REPORT,
                                                                            page=page,
                                                                            key=PaginationKey.ADMIN_REPORT_CHECK).pack()),
        InlineKeyboardButton(text=BT.NEXT, callback_data=PaginationCallback(action=PaginationAction.NEXT,
                                                                            markup=PaginationMarkup.ADMIN_REPORT,
                                                                            page=page,
                                                                            key=PaginationKey.ADMIN_REPORT_CHECK).pack()),
    )

    keyboard.add(
        InlineKeyboardButton(text=BT.CLOSE, callback_data=CallbackConstants.DELETE_MESSAGE)
    )

    return keyboard.adjust(2, 1).as_markup()


async def profile_panel(tg_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=BT.CHANGE_USER_NAME,
                             callback_data=ChangeUserInfoCallback(tg_id=tg_id, change_item=UserChangeItem.NAME).pack()),
    )

    return keyboard.adjust(1).as_markup()
