from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.models import Category
from keyboards import cancel_mk, search_confirm_panel, search_type_panel
from states import AddReceiptForm, SearchReceiptForm

router = Router(name='user_callbacks')


@router.callback_query(AddReceiptForm.category, F.data.startswith('select_category_to_add_receipt_'))
async def choose_category_to_add_receipt(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]
    category = await Category.get(id=category_id)
    await callback.answer(f'Вы перешли в категорию {category.title}')
    await state.update_data(category=category)
    await state.set_state(AddReceiptForm.receipt)
    await callback.message.answer(f'Отлично, вы выбрали категорию <b>{category.title}</b>.\n'
                                  f'Теперь чтобы добавить рецепт, заполните информацию в таком виде (Пробелы после скобок соблюдать!):\n'
                                  f'---------------------------------------------\n'
                                  f'1) Название\n'
                                  f'2) Ссылка на статью с рецептом в https://telegra.ph \n'
                                  f'---------------------------------------------\n'
                                  f'Подробнее про телеграф - https://uchet-jkh.ru/i/telegraf-dlya-telegram-cto-eto-i-kak-ono-rabotaet/', reply_markup=cancel_mk)


@router.callback_query(SearchReceiptForm.category, F.data.startswith('select_category_to_search_receipt_'))
async def choose_category_to_search_receipt(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]
    category = await Category.get(id=category_id)
    await callback.answer(f'Вы перешли в категорию {category.title}')
    await state.update_data(category=category)
    await state.set_state(SearchReceiptForm.search_type)
    await callback.message.answer('Хотите произвести поиск?', reply_markup=search_confirm_panel)


@router.callback_query(SearchReceiptForm.search_type, F.data.startswith('search_input_confirm'))
async def search_type_confirm(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchReceiptForm.result)
    await callback.message.answer('Выберите вариант поиска:', reply_markup=search_type_panel)


@router.callback_query(SearchReceiptForm.search_type, F.data.startswith('search_input_cancel'))
async def search_type_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выполняется вывод рецептов по алфавиту')
    await callback.message.delete()
    await state.update_data(search_type=None)
    await state.set_state(SearchReceiptForm.result)


@router.callback_query(SearchReceiptForm.search_type, F.data.startswith('choose_search_type_by_'))
async def choose_search_type(callback: CallbackQuery, state: FSMContext):
    search_type = callback.data.split('_')[-1]

    if search_type == 'name':
        await callback.answer(f'Вы выбрали поиск по названию')
    else:
        await callback.answer(f'Вы выбрали поиск по автору')

    await state.update_data(search_type=search_type)
    await state.set_state(SearchReceiptForm.result)


