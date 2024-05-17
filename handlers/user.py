from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import cancel_mk, categories
from keyboards.button_text import ButtonText as BT
from database.models import User, Receipt, UserFavouriteReceipt
from states import AddReceiptForm, SearchReceiptForm
from utils import get_main_kb

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


@router.message(F.text == BT.SETTINGS)
@router.message(Command('profile'))
async def settings(message: Message):
    tg_id = message.from_user.id
    user = await User.get(tg_id=tg_id).prefetch_related('favourite_receipts')
    favourite_receipts = await user.favourite_receipts.all().count()
    published_receipts = await Receipt.filter(creator=user).count()
    await message.answer(f'Ваш профиль:\n'
                         f'Имя: <b>{user.name}</b>\n'
                         f'Опубликованные рецепты: <b>{published_receipts}</b>\n'
                         f'Любимые рецепты: <b>{favourite_receipts}</b>')


@router.message(F.text == BT.ADD_RECEIPT)
@router.message(Command('add_receipt'))
async def add_receipt(message: Message, state: FSMContext):
    await state.set_state(AddReceiptForm.category)
    await message.answer('Чтобы добавить рецепт, сначала выберите категорию, в котoрую хотите добавить:',
                         reply_markup=await categories('select_category_to_add_receipt_'))


@router.message(F.text == BT.FAVOURITE_RECEIPTS)
@router.message(Command('fav_receipts'))
async def favourite_receipts(message: Message):
    user = await User.get(tg_id=message.from_user.id)
    favourite_receipts = await user.favourite_receipts.all()

    if not favourite_receipts:
        await message.answer('У вас пока что нет сохраненных рецептов')
        return

    await message.answer('...')


@router.message(F.text == BT.MY_RECEIPTS)
@router.message(Command('my_receipts'))
async def user_receipts(message: Message):
    user = await User.get(tg_id=message.from_user.id)
    created_receipts = await Receipt.filter(creator=user)

    if not created_receipts:
        await message.asnwer('Вы пока что не добавили ни одного рецепта. Чтобы добавить рецепт напишите /add_receipt')
        return

    await message.answer('...')


@router.message(F.text == BT.SEARCH_RECEIPTS)
@router.message(Command('search_receipt'))
async def search_receipt(message: Message, state: FSMContext):
    await message.answer('Выберите категорию, в которой хотите искать рецепт:',
                         reply_markup=await categories('select_category_to_search_receipt_'))
    await state.set_state(SearchReceiptForm.category)
