import asyncio

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.models import Recipe, Report, User
from database.redis_client import rc
from constants.button_text import ButtonText as BT
from constants.factory import RecipeChangeItem, UserChangeItem
from keyboards.inline import repeat_search_panel
from keyboards.reply import cancel_mk, profile_mk
from misc.states import (AddRecipeForm, EditRecipeForm, EditUserForm,
                         GetReportReasonForm, SearchRecipeForm, SetTimerForm, RegisterUserForm)
from misc.utils import (cache_list_update, convert_ids_list_into_objects,
                        get_main_kb, send_user_recipe_info, set_timer, notify_admins)

router = Router(name='states_process')


@router.message(RegisterUserForm.agreement, F.text == BT.AGREE_AGREEMENT)
async def user_agree_agreement(message: Message, state: FSMContext):
    user = message.from_user
    tg_id = user.id
    full_name = user.first_name

    if user.last_name:
        full_name += " " + user.last_name

    await User.create(tg_id=tg_id, name=full_name, username=user.username)
    await message.answer('Вы согласились на условия использования бота.', reply_markup=await get_main_kb(tg_id))
    await state.clear()


@router.message(RegisterUserForm.agreement, F.text != BT.AGREE_AGREEMENT and F.text != '/start')
async def invalid_user_agree_agreement(message: Message, state: FSMContext):
    await message.answer('Вы не согласились, с условиями использования!')


@router.message(AddRecipeForm.title, F.text)
async def process_addrecipeform_title(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        tg_id = message.chat.id
        await message.answer('Отменено.', reply_markup=await get_main_kb(tg_id))
        await state.clear()
        return

    await state.update_data(title=message.text)
    await message.answer(f'Отлично, теперь чтобы добавить рецепт, вам необходимо прислать ссылку на статью в telegra.ph\n\n'
                         f'telegra.ph - Удобный простой редактор статей. Также отлично подойдет для написания рецептов.\n'
                         f'Подробнее про telegra.ph - https://telegra.ph/telegraph-01-25', reply_markup=cancel_mk)
    await state.set_state(AddRecipeForm.url)


@router.message(AddRecipeForm.url, F.text.startswith('https://telegra.ph/'))
async def process_addrecipeform_url(message: Message, state: FSMContext):
    tg_id = message.chat.id
    user = await User.get(tg_id=tg_id)
    data = await state.get_data()
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=await get_main_kb(tg_id))
        await state.clear()
        return

    title = data['title']
    category = data['category']

    if await Recipe.filter(url=message.text).exists():
        await message.answer('Данный рецепт уже добавлен!', reply_markup=cancel_mk)
        return

    await Recipe.create(title=title, url=message.text, creator=user, category=category)
    await message.answer('Рецепт успешно добавлен.', reply_markup=await get_main_kb(tg_id))
    await state.clear()


@router.message(AddRecipeForm.url, ~F.text.startswith('https://telegraph/'))
async def process_invalid_addrecipeform_url(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=await get_main_kb(message.chat.id))
        await state.clear()
        return

    await message.answer('Ссылка должна быть на статью в https://telegra.ph/ !. Повторите попытку.')


@router.message(SearchRecipeForm.process_user_input, F.text)
async def search_recipe_form_by_category(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=await get_main_kb(message.chat.id, only_menu=True))
        await state.set_state(SearchRecipeForm.ask_user_input)
        return

    await message.bot.send_chat_action(chat_id=message.chat.id,
                                       action=ChatAction.TYPING)
    data = await state.get_data()
    search_type = data['search_type']
    category = data['category']
    message_to_delete = data['message']
    prompt = message.text
    if search_type == 'name':
        pre_result = Recipe.filter(title__icontains=prompt, is_active=True)

    else:  # search_type == 'author':
        pre_result = Recipe.filter(creator__name__icontains=prompt, is_active=True)

    ids = await pre_result.all().values_list('id', flat=True)

    if category:
        ids = await pre_result.filter(category=category).values_list('id', flat=True)

    if not ids:
        await message.answer('По вашему запросу ничего не найдено. Введите запрос снова.',
                             reply_markup=repeat_search_panel)
        return

    await message_to_delete.delete()
    
    client = rc.get_client()
    key = f'{message.chat.id}'
    cache_list_update(client, key, ids)
    result = await convert_ids_list_into_objects(ids, Recipe, ['category', 'creator'])
    await send_user_recipe_info(result, message, category, print_find=True)
    await state.clear()


@router.message(SearchRecipeForm.process_user_input, ~F.text)
async def invalid_search_recipe_form(message: Message, state: FSMContext):
    await message.answer('Отправьте текстом!')


@router.message(SetTimerForm.minutes, F.text & F.text.isdigit() & F.text.func(lambda x: int(x) >= 1))
async def set_timer_form(message: Message, state: FSMContext):
    await state.clear()
    minutes = int(message.text)
    await message.answer(f'Таймер установлен на {minutes} минут(ы). По истечению времени вам придет сообщение.',
                         reply_markup=await get_main_kb(message.chat.id))
    await asyncio.create_task(set_timer(message, minutes))


@router.message(SetTimerForm.minutes, ~F.text | ~F.text.isdigit() | F.text.func(lambda x: int(x) <= 0))
async def invalid_set_timer_form(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=await get_main_kb(message.chat.id))
        await state.clear()
        return

    await message.answer('Введите положительное число!')


@router.message(EditRecipeForm.get_user_input)
async def edit_recipe_data(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=await get_main_kb(message.chat.id, only_menu=True))
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
    await message.answer('Данные успешно сохранены!', reply_markup=await get_main_kb(message.chat.id, only_menu=True))
    await state.clear()


@router.message(GetReportReasonForm.reason, F.text)
async def process_reason_input(message: Message, state: FSMContext):
    data = await state.get_data()
    user = data['user']
    recipe = data['recipe']
    reason = message.text

    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=await get_main_kb(message.from_user.id, True))
        await state.clear()
        return

    await Report.create(user=user, recipe=recipe, reason=reason)

    if await Report.filter(recipe=recipe).count() >= 3:
        await notify_admins(message.bot, f'<b>Новые жалобы!</b>\n'
                                         f'На рецепт {recipe.url}')
    await message.answer('Ваша жалоба записана.', reply_markup=await get_main_kb(message.from_user.id, True))
    await state.clear()


@router.message(GetReportReasonForm.reason, ~F.text)
async def invalid_reason_input(message: Message):
    await message.answer('Введите текст!')


@router.message(EditUserForm.get_user_input, F.text)
async def process_edituserform_getuserinput(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=profile_mk)
        await state.clear()
        return

    data = await state.get_data()
    user = data['user']
    change_item = data['change_item']

    if change_item == UserChangeItem.NAME:
        user.name = message.text

    await user.save()
    await message.answer('Данные успешно изменены!', reply_markup=profile_mk)
    await state.clear()
