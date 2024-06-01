from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.button_text import ButtonText as BT
from keyboards.factories import DeleteRecipeCallback
from keyboards.constants import DeleteRecipeAction

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

confirm_delete_recipe = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.CONFIRM,
                                 callback_data=DeleteRecipeCallback(action=DeleteRecipeAction.CONFIRM).pack()),
            InlineKeyboardButton(text=BT.CANCEL,
                                 callback_data=DeleteRecipeCallback(action=DeleteRecipeAction.CANCEL).pack())
        ]
    ]
)

