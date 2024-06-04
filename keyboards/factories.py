from aiogram.filters.callback_data import CallbackData

from keyboards.constants import (PaginationAction,
                                 PaginationMarkup,
                                 RecipeChangeItem, SearchType, BackToType, )


class RecipePaginationCallback(CallbackData, prefix='pag'):
    page: int
    action: PaginationAction
    markup: PaginationMarkup


class AddRecipeToFavouritesCallback(CallbackData, prefix='add_to_fav'):
    recipe_id: int
    page: int
    single_recipe_view: bool


class ReportRecipeCallback(CallbackData, prefix='report_recipe'):
    recipe_id: int


class ChangeRecipeInfoCallback(CallbackData, prefix='change_recipe_info'):
    recipe_id: int
    change_item: RecipeChangeItem


class DeleteRecipeCallback(CallbackData, prefix='delete_recipe'):
    # recipe_id in state data
    action: str


class BackCallback(CallbackData, prefix='back_to_choose_category'):
    back_to_type: BackToType
    change_kb: bool


class ChooseSearchTypeCallback(CallbackData, prefix='choose_search_type'):
    type: SearchType
