from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callback import CallbackConstants
from bot.constants.button_text import ButtonText as BT
from bot.keyboards.factories import BackCallback, DeleteItemCallback
from bot.constants.factory import DeleteAction, BackToType

confirm_delete_recipe = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.CONFIRM,
                                 callback_data=DeleteItemCallback(action=DeleteAction.CONFIRM).pack()),
            InlineKeyboardButton(text=BT.CANCEL,
                                 callback_data=DeleteItemCallback(action=DeleteAction.CANCEL).pack())
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


user_agreement_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.READ_AGREEMENT, url='https://telegra.ph/Agreement-06-09-6')
        ]
    ]
)

admin_manage_category_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.CHANGE_CATEGORY, callback_data=CallbackConstants.EDIT_CATEGORY),
        ],
        [
            InlineKeyboardButton(text=BT.ADD_CATEGORY, callback_data=CallbackConstants.ADD_CATEGORY),
        ]
    ]
)
