from aiogram.fsm.state import StatesGroup, State


class AddRecipeForm(StatesGroup):
    category = State()
    title = State()
    url = State()


class SearchRecipeForm(StatesGroup):
    search_type = State()
    category = State()
    ask_user_input = State()
    process_user_input = State()


class EditRecipeForm(StatesGroup):
    get_user_input = State()
    category = State()


class SetTimerForm(StatesGroup):
    minutes = State() # get_user_input


class DeleteRecipeForm(StatesGroup):
    confirm = State()


class GetReportReasonForm(StatesGroup):
    reason = State()


class GetWarnReasonForm(StatesGroup):
    reason = State()


class EditUserForm(StatesGroup):
    get_user_input = State()


class RegisterUserForm(StatesGroup):
    agreement = State()


class EditCategoryForm(StatesGroup):
    choose_category = State()
    get_user_input = State()


class AddCategoryForm(StatesGroup):
    get_user_input = State()


class DeleteCategoryForm(StatesGroup):
    confirm = State()
