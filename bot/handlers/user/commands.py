import random

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.models import Recipe, User
from bot.database.redis_client import rc
from bot.keyboards import cancel_mk, help_kb, profile_mk, search_type_panel, user_agreement_panel, \
    user_agree_agreement_kb, random_recipe_kb
from bot.keyboards.builders import categories, profile_panel
from bot.constants.button_text import ButtonText as BT
from bot.misc.filters import IsNotActiveUser
from bot.misc.states import (AddRecipeForm, RegisterUserForm, SearchRecipeForm,
                             SetTimerForm)
from bot.misc.utils import (cache_list_update, convert_ids_list_into_objects,
                            get_main_kb, send_single_recipe,
                            send_user_recipe_change, send_user_recipe_info)

router = Router(name='user_handlers')


@router.message(IsNotActiveUser())
@router.message(IsNotActiveUser(), F.text == BT.DEATH)
async def handle_not_active_user(message: Message):
    user = await User.get(tg_id=message.from_user.id)
    await message.answer(f'<b>Уважаемый пользователь {user.name}! </b>\n'
                         f'Ваш акканут был заблокирован администрацией за трехкратное нарушение правил.\n',
                         reply_markup=help_kb)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    user = message.from_user

    tg_id = user.id
    full_name = user.first_name

    if user.last_name:
        full_name += " " + user.last_name

    user = await User.get_or_none(tg_id=tg_id)
    if not user:
        await message.answer(f'<b>{full_name}, добро пожаловать в нашего бота!</b>\n'
                             f'Перед тем как начать им пользоваться вам необходимо '
                             f'ознакомиться с условиями использования бота.',
                             reply_markup=user_agreement_panel)
        await message.answer('НАЖИМАЯ НА КНОПКУ НИЖЕ, ВЫ СОГЛАШАЕТЕСЬ С УСЛОВИЯМИ ИСПОЛЬЗОВАНИЯ БОТА.',
                             reply_markup=user_agree_agreement_kb)
        await state.set_state(RegisterUserForm.agreement)
    else:
        await message.answer(f'С возвращением, @{user.username}!', reply_markup=await get_main_kb(user.tg_id))


@router.message(F.text == BT.MAIN_MENU)
@router.message(Command('menu'))
async def menu(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    await state.clear()
    await message.answer('🏠 Вы перешли в главное меню', reply_markup=await get_main_kb(tg_id))


@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Команды для использования бота:\n'
                         '<b>/menu</b> - Переход в главное меню\n'
                         '<b>/timer</b> - Поставить таймер\n'
                         '<b>/profile</b> - Просмотр профиля\n'
                         '<b>/my_recipes</b> - Просмотр созданных рецептов\n'
                         '<b>/fav_recipes</b> - Просмотр сохраненных рецептов\n'
                         '<b>/search_recipe</b> - Поиск рецептов\n'
                         '<b>/random_recipe</b> - Случайный рецепт\n'
                         '<b>/fast_search *ваш запрос*</b> - Быстрый поиск рецептов по названию\n'
                         '<b>/help - Просмотр данного сообщения.</b>')


@router.message(F.text == BT.TIMER)
@router.message(Command('timer'))
async def set_timer(message: Message, state: FSMContext):
    await message.answer('Введите пожалуйста время в минутах:', reply_markup=cancel_mk)
    await state.set_state(SetTimerForm.minutes)


@router.message(F.text == BT.PROFILE)
@router.message(Command('profile'))
async def profile(message: Message):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id).prefetch_related('favourite_recipes')
    favourite_recipes = await user.favourite_recipes.all().count()
    published_recipes = await Recipe.filter(creator=user).count()
    await message.answer('Вы перешли в свой профиль.', reply_markup=profile_mk)
    await message.answer(f'🧑 Ваш профиль\n'
                         f'👀 Имя: <b>{user.name}</b>\n'
                         f'📚 Опубликованные рецепты: <b>{published_recipes}</b>\n'
                         f'♥ Любимые рецепты: <b>{favourite_recipes}</b>',
                         reply_markup=await profile_panel(tg_id))


@router.message(F.text == BT.ADD_RECIPE)
@router.message(Command('add_recipe'))
async def add_recipe(message: Message, state: FSMContext):
    await state.set_state(AddRecipeForm.category)
    await message.answer('Вы перешли к выбору категории.', reply_markup=await get_main_kb(message.chat.id, True))
    await message.answer('Чтобы добавить рецепт, сначала выберите категорию, в котoрую хотите добавить:',
                         reply_markup=await categories('select_category_to_add_recipe_', prev=False))


@router.message(F.text == BT.FAVOURITE_RECIPES)
@router.message(Command('fav_recipes'))
async def favourite_recipes(message: Message):
    tg_id = str(message.from_user.id)
    user = await User.get(tg_id=tg_id).prefetch_related('favourite_recipes')
    ids = await user.favourite_recipes.filter(is_active=True).prefetch_related('category', 'creator').values_list('id', flat=True)

    if not ids:
        await message.answer('У вас пока что нет сохраненных рецептов')
        return

    client = rc.get_client()
    cache_list_update(client, tg_id, ids)
    favourite_recipes = await convert_ids_list_into_objects(ids, Recipe, ['category', 'creator'])

    await message.answer(f'У вас {len(favourite_recipes)} сохраненных рецептов.')
    await send_user_recipe_info(favourite_recipes, message, print_find=False)


@router.message(F.text == BT.MY_RECIPES)
@router.message(Command('my_recipes'))
async def user_recipes(message: Message):
    tg_id = str(message.from_user.id)
    client = rc.get_client()
    user = await User.get(tg_id=message.from_user.id)
    ids = await Recipe.filter(creator=user).values_list('id', flat=True)

    if not ids:
        await message.answer('Вы пока что не добавили ни одного рецепта. Чтобы добавить рецепт напишите /add_recipe')
        return

    cache_list_update(client, tg_id, ids)
    created_recipes = await convert_ids_list_into_objects(ids, Recipe, ['category', 'creator'])

    await message.answer(f'У вас {len(created_recipes)} созданных рецептов.')
    await send_user_recipe_change(created_recipes, message)


@router.message(F.text == BT.SEARCH_RECIPES)
@router.message(Command('search_recipe'))
async def search_recipe(message: Message, state: FSMContext):
    await message.answer('Вы перешли к выбору варианта поиска.', reply_markup=await get_main_kb(message.from_user.id, True))
    await message.answer('Выберите вариант поиска:', reply_markup=await search_type_panel())
    await state.set_state(SearchRecipeForm.search_type)


@router.message(F.text == BT.RANDOM_RECIPE)
@router.message(Command('random_recipe'))
async def random_recipe(message: Message):
    all_recipes = await Recipe.all().prefetch_related('creator', 'category')
    recipe = random.choice(all_recipes)
    await message.answer('Случайный рецепт', reply_markup=random_recipe_kb)
    await send_single_recipe(recipe, message)


@router.message(Command('fast_search'))
async def fast_search(message: Message, command: CommandObject):
    prompt = command.args

    if not prompt:
        await message.answer('Введите поисковой запрос после команды.\n'
                             'Пример:\n'
                             '<b>/fast_search</b> Пельмени', reply_markup=await get_main_kb(message.from_user.id, True))
        return

    recipe = await Recipe.filter(title__icontains=prompt).first().prefetch_related('creator', 'category')
    if recipe:
        await send_single_recipe(recipe, message)
    else:
        await message.answer('По вашему запросу рецептов не найдено.', reply_markup=await get_main_kb(message.from_user.id, True))


@router.message()
async def handle_all_messages(message: Message):
    await message.reply('Извините, мне такая команда неизвестна.')
