from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from bot.constants.button_text import ButtonText as BT

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
            KeyboardButton(text=BT.RANDOM_RECIPE),
        ],
        [
            KeyboardButton(text=BT.ADMIN_INTERFACE),
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
        ],
        [
            KeyboardButton(text=BT.RANDOM_RECIPE),
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
        # [
        #     KeyboardButton(text=BT.ADMIN_PANEL),
        # ],
        [
            KeyboardButton(text=BT.MANAGE_CATEGORIES),
        ],
        [
            KeyboardButton(text=BT.USER_INTERFACE),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Главное меню',
)

cancel_or_skip_kb = ReplyKeyboardMarkup(
    keyboard=[
        # [
        #     KeyboardButton(text=BT.SKIP),
        # ],
        [
            KeyboardButton(text=BT.CANCEL),
        ]
    ],
    resize_keyboard=True,
)

help_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.DEATH)
        ]
    ],
    resize_keyboard=True,
)

user_agree_agreement_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.AGREE_AGREEMENT)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Соглашение.'
)

random_recipe_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.RANDOM_RECIPE)
        ],
        [
            KeyboardButton(text=BT.MAIN_MENU)
        ]
    ],
    resize_keyboard=True
)
