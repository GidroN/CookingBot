from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .button_text import ButtonText as BT

rmk = ReplyKeyboardRemove()

only_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.MAIN_MENU)
        ],
    ],
    resize_keyboard=True,
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

main_menu_user_with_admin_option_kb = ReplyKeyboardMarkup(
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
            KeyboardButton(text=BT.ADMIN_PANEL),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Главное меню'
)


main_menu_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.SEARCH_RECIPES),
            KeyboardButton(text=BT.ADD_RECIPE),
        ],
        [
            KeyboardButton(text=BT.PROFILE),
            KeyboardButton(text=BT.TIMER),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Главное меню',
)

main_menu_admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.CHECK_REPORTS),
        ],
        [
            KeyboardButton(text=BT.USER_PANEL),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Главное меню',
)
