from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .button_text import ButtonText as BT

rmk = ReplyKeyboardRemove()

main_menu_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.SEARCH_RECIPES),
            KeyboardButton(text=BT.ADD_RECIPE),
        ],
        [
            KeyboardButton(text=BT.PROFILE),
            KeyboardButton(text=BT.TIMER),
        ],
        [
            KeyboardButton(text=BT.MAIN_MENU),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Главное меню',
)

profile_mk = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.FAVOURITE_RECIPES),
            KeyboardButton(text=BT.MY_RECIPES)
        ],
        [
            KeyboardButton(text=BT.MAIN_MENU),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите опцию'
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
