import asyncio

from aiogram import Router, F, Bot
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import Message

from keyboards import cancel_mk
from keyboards.constants import RecipeChangeItem
from keyboards.button_text import ButtonText as BT
from database.models import User, Recipe
from database.redis_client import rc
from misc.states import AddRecipeForm, SearchRecipeForm, SetTimerForm, EditRecipeForm, DeleteRecipeForm
from misc.utils import extract_recipe_info, get_main_kb, set_timer, send_user_recipe_info, \
    convert_ids_list_into_objects, cache_list_update

router = Router(name='states_process')


# @router.message(AddRecipeForm.recipe, F.text)
# async def add_recipe_form(message: Message, state: FSMContext):
#     tg_id = message.from_user.id
#     if message.text == BT.CANCEL:
#         await message.answer('Отменено.', reply_markup=get_main_kb(tg_id))
#         await state.clear()
#         return
#
#     title, url = extract_recipe_info(message.text)
#     if not url.startswith('https://telegra.ph'):
#         await message.answer('Ссылка должна быть на статью в телеграф!!')
#         return
#
#     user = await User.get(tg_id=tg_id)
#     category = (await state.get_data())['category']
#
#     await Recipe.create(title=title, url=url, creator=user, category=category)
#     await message.answer('Рецепт успешно добавлен!', reply_markup=get_main_kb(tg_id))
#     await state.clear()


# @router.message(AddRecipeForm.recipe, ~F.text)
# async def invalid_add_recipe_form(message: Message, state: FSMContext):
#     await message.answer('Принимается только текст.')


@router.message(AddRecipeForm.title, F.text)
async def process_addrecipeform_title(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        tg_id = message.chat.id
        await message.answer('Отменено.', reply_markup=get_main_kb(tg_id))
        await state.clear()
        return

    await state.update_data(title=message.text)
    await message.answer(f'Отлично, теперь пришлите ссылку на сам рецепт в telegra.ph', reply_markup=cancel_mk)
    await state.set_state(AddRecipeForm.url)


@router.message(AddRecipeForm.url, F.text)
async def process_addrecipeform_url(message: Message, state: FSMContext):
    tg_id = message.chat.id
    user = await User.get(tg_id=tg_id)
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=get_main_kb(tg_id))
        await state.clear()
        return

    title = (await state.get_data())['title']
    if Recipe.filter(url=message.text).exists():
        await message.answer('Данный рецепт уже добавлен!', reply_markup=cancel_mk)
        return

    await Recipe.create(title=title, url=message.text, user=user)
    await message.answer('Рецепт успешно добавлен.', reply_markup=get_main_kb(tg_id))
    await state.clear()


@router.message(SearchRecipeForm.get_user_input, F.text)
async def search_recipe_form_by_category(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=get_main_kb(message.chat.id, only_menu=True))
        await state.set_state(SearchRecipeForm.search_type)
        return

    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.TYPING)
    search_type = (await state.get_data())['search_type']
    category = (await state.get_data())['category']
    prompt = message.text

    if search_type == 'name':
        pre_result = Recipe.filter(title__icontains=prompt)

    else:  # search_type == 'author':
        pre_result = Recipe.filter(creator__name__icontains=prompt)

    ids = await pre_result.all().values_list('id', flat=True)

    if category:
        ids = await pre_result.filter(category=category).values_list('id', flat=True)

    if not ids:
        await message.answer('По вашему запросу не найдено рецептов. Повторите попытку.',
                             reply_markup=get_main_kb(message.chat.id, True))
        return

    client = rc.get_client()
    key = str(message.chat.id)
    cache_list_update(client, key, ids)
    result = await convert_ids_list_into_objects(ids, Recipe, ['category', 'creator'])
    await send_user_recipe_info(result, message, category)
    await state.clear()


@router.message(SearchRecipeForm.get_user_input, ~F.text)
async def invalid_search_recipe_form(message: Message, state: FSMContext):
    await message.answer('Отправьте текстом!')


@router.message(SetTimerForm.minutes, F.text & F.text.isdigit() & F.text.func(lambda x: int(x) >= 1))
async def set_timer_form(message: Message, state: FSMContext):
    await state.clear()
    minutes = int(message.text)
    await message.answer(f'Таймер установлен на {minutes} минут(ы). По истечению времени вам придет сообщение.',
                         reply_markup=get_main_kb(message.chat.id))
    await asyncio.create_task(set_timer(message, minutes))


@router.message(SetTimerForm.minutes, ~F.text | ~F.text.isdigit())
async def invalid_set_timer_form(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=get_main_kb(message.chat.id))
        await state.clear()
        return

    await message.answer('Введите положительное число!')


@router.message(EditRecipeForm.get_user_input)
async def edit_recipe_data(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=get_main_kb(message.chat.id, only_menu=True))
        await state.clear()
        return

    data = await state.get_data()
    change_item = data['change_item']
    recipe_id = data['recipe_id']
    recipe = await Recipe.get(id=recipe_id)

    if change_item == RecipeChangeItem.NAME:
        recipe.title = message.text
    else:  # change_item == RecipeChangeItem.LINK:
        recipe.url = message.text

    await recipe.save()
    await message.answer('Данные успешно сохранены!', reply_markup=get_main_kb(message.chat.id, only_menu=True))
    await state.clear()
