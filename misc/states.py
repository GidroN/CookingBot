from aiogram.fsm.state import StatesGroup, State


class AddRecipeForm(StatesGroup):
    category = State()
    recipe = State()


class SearchRecipeForm(StatesGroup):
    category = State()
    search_type = State()
    get_user_input = State()
    # result = State()


class SetTimerForm(StatesGroup):
    minutes = State() # get_user_input
