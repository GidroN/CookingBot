from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .button_text import ButtonText as BT

rmk = ReplyKeyboardRemove()

main_menu_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.SEARCH_RECEIPTS),
            KeyboardButton(text=BT.ADD_RECEIPT),
        ],
        [
            KeyboardButton(text=BT.FAVOURITE_RECEIPTS),
            KeyboardButton(text=BT.MY_RECEIPTS),
        ],
        [
            KeyboardButton(text=BT.SETTINGS),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Главное меню',
)

cancel_mk = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.CANCEL),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)