from aiogram.fsm.state import StatesGroup, State


class AddReceiptForm(StatesGroup):
    category = State()
    receipt = State()


class SearchReceiptForm(StatesGroup):
    category = State()
    search_type = State()
    result = State()
