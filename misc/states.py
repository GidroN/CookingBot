from aiogram.fsm.state import StatesGroup, State


class AddRecipeForm(StatesGroup):
    category = State()
    recipe = State()


class SearchRecipeForm(StatesGroup):
    category = State()
    search_type = State()
    get_user_input = State()


class EditRecipeForm(StatesGroup):
    get_user_input = State()
    category = State()


class SetTimerForm(StatesGroup):
    minutes = State() # get_user_input


class DeleteRecipeForm(StatesGroup):
    confirm = State()