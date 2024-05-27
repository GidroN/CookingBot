from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import cancel_mk, categories, profile_mk, user_recipe_panel, my_recipe_edit_panel
from keyboards.button_text import ButtonText as BT
from database.models import User, Recipe, UserFavouriteRecipe
from misc.states import AddRecipeForm, SearchRecipeForm, SetTimerForm
from misc.utils import get_main_kb, send_user_recipe_info
from database.redis_client import rc

router = Router(name='user_handlers')


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    tg_id = user.id
    full_name = user.first_name

    if user.last_name:
        full_name += " " + user.last_name

    username = user.username
    reply_mk = get_main_kb(tg_id)

    if username:
        await message.answer(f'Добро пожаловать, @{user.username}!', reply_markup=reply_mk)
    else:
        await message.answer(f'Добро пожаловать!', reply_markup=reply_mk)

    if not await User.filter(tg_id=tg_id).exists():
        await User.create(tg_id=tg_id, name=full_name.strip(), username=username)


@router.message(F.text == BT.MAIN_MENU)
@router.message(Command('menu'))
async def menu(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    await state.clear()
    await message.answer('🏠 Вы перешли в главное меню', reply_markup=get_main_kb(tg_id))


@router.message(F.text == BT.TIMER)
@router.message(Command('timer'))
async def set_timer(message: Message, state: FSMContext):
    await message.answer('Введите пожалуйста время в минутах:', reply_markup=cancel_mk)
    await state.set_state(SetTimerForm.minutes)


@router.message(F.text == BT.PROFILE)
@router.message(Command('profile'))
async def settings(message: Message):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id).prefetch_related('favourite_recipes')
    favourite_recipes = await user.favourite_recipes.all().count()
    published_recipes = await Recipe.filter(creator=user).count()
    await message.answer(f'Ваш профиль:\n'
                         f'Имя: <b>{user.name}</b>\n'
                         f'Опубликованные рецепты: <b>{published_recipes}</b>\n'
                         f'Любимые рецепты: <b>{favourite_recipes}</b>', reply_markup=profile_mk)


@router.message(F.text == BT.ADD_RECIPE)
@router.message(Command('add_recipe'))
async def add_recipe(message: Message, state: FSMContext):
    await state.set_state(AddRecipeForm.category)
    await message.answer('Чтобы добавить рецепт, сначала выберите категорию, в котoрую хотите добавить:',
                         reply_markup=await categories('select_category_to_add_recipe_'))


@router.message(F.text == BT.FAVOURITE_RECIPES)
@router.message(Command('fav_recipes'))
async def favourite_recipes(message: Message):
    user = await User.get(tg_id=message.from_user.id).prefetch_related('favourite_recipes')
    favourite_recipes = await user.favourite_recipes.all().prefetch_related('recipe')

    if not favourite_recipes:
        await message.answer('У вас пока что нет сохраненных рецептов')
        return

    await message.answer(f'У вас {len(favourite_recipes)} сохраненных рецептов.')
    await send_user_recipe_info(favourite_recipes, message, print_find=False)


@router.message(F.text == BT.MY_RECIPES)
@router.message(Command('my_recipes'))
async def user_recipes(message: Message):
    user = await User.get(tg_id=message.from_user.id)
    created_recipes = await Recipe.filter(creator=user)

    if not created_recipes:
        await message.answer('Вы пока что не добавили ни одного рецепта. Чтобы добавить рецепт напишите /add_recipe')
        return

    result = await Recipe.filter(creator__tg_id=message.chat.id).prefetch_related('creator')

    # await message.answer(f'У вас {len(favourite_recipes)} сохраненных рецептов.')
    # await send_user_recipe_info(favourite_recipes, message, print_find=False)


@router.message(F.text == BT.SEARCH_RECIPES)
@router.message(Command('search_recipe'))
async def search_recipe(message: Message, state: FSMContext):
    await message.answer('Вы перешли к выбору категории.', reply_markup=get_main_kb(message.chat.id, True))
    await message.answer('Выберите категорию, в которой хотите искать рецепт:',
                         reply_markup=await categories('select_category_to_search_recipe_', show_all_recipes=True))
    await state.set_state(SearchRecipeForm.category)
