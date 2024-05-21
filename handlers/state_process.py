import asyncio

from aiogram import Router, F, Bot
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import recipe_panel
from keyboards.button_text import ButtonText as BT
from database.models import User, Recipe, Category
from states import AddRecipeForm, SearchRecipeForm, SetTimerForm
from utils import extract_recipe_info, get_main_kb, set_timer

router = Router(name='states_process')


@router.message(AddRecipeForm.recipe, F.text)
async def add_recipe_form(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=get_main_kb(tg_id))
        await state.clear()
        return

    title, url = extract_recipe_info(message.text)
    if not url.startswith('https://telegra.ph'):
        await message.answer('Ссылка должна быть на статью в телеграф!!')
        return

    user = await User.get(tg_id=tg_id)
    category = (await state.get_data())['category']

    await Recipe.create(title=title, url=url, creator=user, category=category)
    await message.answer('Рецепт успешно добавлен!', reply_markup=get_main_kb(tg_id))
    await state.clear()


@router.message(AddRecipeForm.recipe, ~F.text)
async def invalid_add_recipe_form(message: Message, state: FSMContext):
    await message.answer('Принимается только текст.')


@router.message(SearchRecipeForm.get_user_input, F.text)
async def search_recipe_form_by_category(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=get_main_kb(message.chat.id))
        await state.set_state(SearchRecipeForm.search_type)
        return

    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.TYPING)
    search_type = (await state.get_data())['search_type']
    category = (await state.get_data())['category']
    prompt = message.text

    result = []
    if search_type == 'name':
        result = await Recipe.filter(title__icontains=prompt, category=category).prefetch_related('creator')
    elif search_type == 'author':
        result = await Recipe.filter(creator__name__icontains=prompt, category=category).prefetch_related('creator')

    # if category:
    #     result = await result.filter(category=category)

    recipes_found = len(result)
    count = 1
    for recipe in result:
        if count == 5:
            await message.answer('...')
            return

        await message.answer(f'<b>{recipe.title}</b>\n'
                             f'Автор: {recipe.creator.name}\n'
                             f'{recipe.url}', reply_markup=recipe_panel)
        count += 1

    await message.answer(f'Найдено {recipes_found} рецептов', reply_markup=get_main_kb(message.chat.id))
    await state.set_state(SearchRecipeForm.search_type)


@router.message(SearchRecipeForm.result, ~F.text)
async def invalid_search_recipe_form(message: Message, state: FSMContext):
    await message.answer('Отправьте текстом!')


@router.message(SetTimerForm.minutes, F.text & F.text.isdigit() & F.text.func(lambda x: int(x) >= 1))
async def set_timer_form(message: Message, state: FSMContext):
    await state.clear()
    minutes = int(message.text)
    await message.answer(f'Таймер установлен на {minutes} минут(ы). По истечению времени вам придет сообщение.', reply_markup=get_main_kb(message.chat.id))
    await asyncio.create_task(set_timer(message, minutes))


@router.message(SetTimerForm.minutes, ~F.text | ~F.text.isdigit())
async def invalid_set_timer_form(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=get_main_kb(message.chat.id))
        await state.clear()
        return

    await message.answer('Введите положительное число!')
