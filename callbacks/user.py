from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.models import Category
from keyboards import cancel_mk, search_type_panel, categories
from keyboards.button_text import ButtonText as BT
from states import AddRecipeForm, SearchRecipeForm
from utils import get_main_kb

router = Router(name='user_callbacks')


@router.message(F.text == BT.MAIN_MENU)
@router.message(Command('menu'))
async def menu(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    await state.clear()
    await message.answer('🏠 Вы перешли в главное меню', reply_markup=get_main_kb(tg_id))


@router.callback_query(AddRecipeForm.category, F.data.startswith('select_category_to_add_recipe_'))
async def choose_category_to_add_recipe(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]
    category = await Category.get(id=category_id)
    await callback.answer(f'Вы перешли в категорию {category.title}')
    await state.update_data(category=category)
    await state.set_state(AddRecipeForm.recipe)
    await callback.message.answer(f'Отлично, вы выбрали категорию <b>{category.title}</b>.\n'
                                  f'Теперь чтобы добавить рецепт, заполните информацию в таком виде (Пробелы после скобок соблюдать!):\n'
                                  f'---------------------------------------------\n'
                                  f'1) Название\n'
                                  f'2) Ссылка на статью с рецептом в https://telegra.ph \n'
                                  f'---------------------------------------------\n'
                                  f'Подробнее про телеграф - https://uchet-jkh.ru/i/telegraf-dlya-telegram-cto-eto-i-kak-ono-rabotaet/', reply_markup=cancel_mk)


@router.callback_query(SearchRecipeForm.category, F.data.startswith('select_category_to_search_recipe_'))
async def choose_category_to_search_recipe(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]

    if category_id.isdigit():
        category = await Category.get(id=category_id)
        await callback.answer(f'Вы перешли в категорию {category.title}')
        await state.update_data(category=category)
    elif category_id == 'all':
        await state.update_data(category=None)

    await callback.message.edit_text('Как хотите произвести поиск?')
    await callback.message.edit_reply_markup(reply_markup=search_type_panel)
    await state.set_state(SearchRecipeForm.search_type)


@router.callback_query(SearchRecipeForm.search_type, F.data == 'back_to_choose_category')
async def back_to_choose_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы вернулись к выбору категории.')
    await callback.message.edit_text('Выберите категорию в которой хотите искать рецепт:')
    await callback.message.edit_reply_markup(reply_markup=await categories('select_category_to_search_recipe_', show_all_recipes=True))
    await state.set_state(SearchRecipeForm.category)


@router.callback_query(SearchRecipeForm.search_type, F.data.startswith('choose_search_type_by_'))
async def choose_search_type(callback: CallbackQuery, state: FSMContext, bot: Bot):
    search_type = callback.data.split('_')[-1]

    if search_type == 'name':
        await callback.answer(f'Вы выбрали поиск по названию.')
        await callback.message.answer('Введите пожалуйста название рецепта', reply_markup=cancel_mk)

    elif search_type == 'author':
        await callback.answer(f'Вы выбрали поиск по автору')
        await callback.message.answer('Введите пожалуйста запрос.', reply_markup=cancel_mk)

    else:
        # search_type = all
        await callback.answer('Производится поиск по самым недавним рецептам.')
        await state.update_data(result='latest', search_type=search_type)
        await state.set_state(SearchRecipeForm.result)
        return

    await state.set_state(SearchRecipeForm.get_user_input)
    await state.update_data(search_type=search_type)



