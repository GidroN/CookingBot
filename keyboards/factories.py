from aiogram.filters.callback_data import CallbackData

from keyboards.constants import (PaginationAction,
                                 PaginationMarkup,
                                 RecipeChangeItem,)


class RecipePaginationCallback(CallbackData, prefix='pag'):
    page: int
    action: PaginationAction
    markup: PaginationMarkup


class AddRecipeToFavouritesCallback(CallbackData, prefix='add_to_fav'):
    recipe_id: int
    page: int


class ReportRecipeCallback(CallbackData, prefix='report_recipe'):
    recipe_id: int


class ChangeRecipeInfoCallback(CallbackData, prefix='change_recipe_info'):
    recipe_id: int
    change_item: RecipeChangeItem


class DeleteRecipeCallback(CallbackData, prefix='delete_recipe'):
    # recipe_id in state data
    action: str
