from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.button_text import ButtonText as BT
from database.models import User, Receipt, Category
from states import AddReceiptForm
from utils import extract_recipe_info, get_main_kb

router = Router(name='states_process')


@router.message(AddReceiptForm.receipt, F.text)
async def add_receipt_form(message: Message, state: FSMContext):
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

    await Receipt.create(title=title, url=url, creator=user, category=category)
    await message.answer('Рецепт успешно добавлен!', reply_markup=get_main_kb(tg_id))
    await state.clear()


@router.message(AddReceiptForm.receipt, ~F.text)
async def invalid_add_receipt_form(message: Message, state: FSMContext):
    await message.answer('Принимается только текст.')

