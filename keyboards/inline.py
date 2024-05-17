from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.button_text import ButtonText as BT
from database.models import Category, Receipt


async def categories(prefix: str):
    all_categories = await Category.all()
    keyboard = InlineKeyboardBuilder()
    for item in all_categories:
        category_items = await Receipt.filter(category=item).count()
        keyboard.add(InlineKeyboardButton(text=f"{item.title} ({category_items})", callback_data=f'{prefix}{item.id}'))
    return keyboard.adjust(1).as_markup()


search_confirm_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.CONFIRM, callback_data='search_input_confirm'),
            InlineKeyboardButton(text=BT.CANCEL, callback_data='search_input_cancel')
        ],
    ]
)

search_type_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Поиск по названию", callback_data='choose_search_type_by_name')
        ],
        [
            InlineKeyboardButton(text="Поиск по автору", callback_data='choose_search_type_by_author')
        ],
    ]
)
