from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.callback_constants import CallbackConstants
from keyboards.button_text import ButtonText as BT
from keyboards.factories import BackCallback, DeleteRecipeCallback
from keyboards.factory_constants import DeleteRecipeAction, BackToType

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

repeat_search_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.SEARCH_REPEAT,
                                 callback_data=BackCallback(back_to_type=BackToType.CHOOSE_SEARCH_TYPE,
                                                            change_kb=True).pack())
        ]
    ]
)


admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.GET_RECIPE_BY_ID, callback_data='g')
        ],
        [
            InlineKeyboardButton(text=BT.GET_USER_BY_ID, callback_data='g'),
        ],
    ]
)
