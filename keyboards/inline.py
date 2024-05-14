from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

links_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Github', url='https://github.com/gidron'),
            InlineKeyboardButton(text='VK', url='https://vk.com/gidron_off'),
        ],
        [
            InlineKeyboardButton(text='Telegram', url='tg://resolve?domain=gidronn'),
        ]
    ]
)

app_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Open App', web_app=WebAppInfo(url=''))
        ]
    ]
)
