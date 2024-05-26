from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class PaginationAction(StrEnum):
    prev = 'prev'
    next = 'next'


class RecipePaginationCallback(CallbackData, prefix='pag'):
    page: int
    action: PaginationAction


class AddRecipeToFavouritesCallback(CallbackData, prefix='add_to_fav'):
    recipe_id: int
    page: int


class ReportRecipeCallback(CallbackData, prefix='report_recipe'):
    recipe_id: int

