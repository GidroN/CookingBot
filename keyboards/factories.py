from aiogram.filters.callback_data import CallbackData

from keyboards.factory_constants import (PaginationAction,
                                         PaginationMarkup,
                                         RecipeChangeItem,
                                         SearchType,
                                         BackToType,
                                         ChooseSearchTypeAction,
                                         PaginationKey, UserChangeItem, )


class PaginationCallback(CallbackData, prefix='pag'):
    page: int
    key: PaginationKey
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


class BackCallback(CallbackData, prefix='back_to'):
    back_to_type: BackToType
    change_kb: bool


class ChooseSearchTypeCallback(CallbackData, prefix='choose_search_type'):
    type: SearchType


 # After choosing category
class ChooseSearchTypeByCategoryCallback(CallbackData, prefix='choose_search_type_by_category'):
    # category_id in state data
    search_type: ChooseSearchTypeAction


class CheckReportsCallback(CallbackData, prefix='check_reports'):
    recipe_id: int


class FalseAlarmRecipeCallback(CallbackData, prefix='false_alarm'):
    recipe_id: int


class WarnUserCallback(CallbackData, prefix='warn_user'):
    recipe_id: int


class ChangeUserInfoCallback(CallbackData, prefix='change_user_info'):
    tg_id: int
    change_item: UserChangeItem
