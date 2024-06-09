from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.models import Recipe, User, UserWarn
from database.redis_client import rc
from keyboards.button_text import ButtonText as BT
from misc.states import GetWarnReasonForm
from misc.utils import (cache_list_update, convert_ids_list_into_objects,
                        get_list_from_cache, get_main_kb,
                        send_recipe_to_check_reports)

router = Router(name='admin_state_process')


@router.message(GetWarnReasonForm.reason, F.text)
async def process_getwarnreasonform_reason(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=await get_main_kb(message.from_user.id, True))
        await state.clear()
        return

    client = rc.get_client()
    data = await state.get_data()
    user = data['user']
    recipe = data['recipe']
    message_to_delete = data['message']
    admin = await User.get(tg_id=message.from_user.id)

    reports_key = f'{message.from_user.id}!reports'
    key = str(message.from_user.id)

    ids = get_list_from_cache(client, key, int)
    ids.remove(recipe.id)
    cache_list_update(client, key, ids)
    recipes = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
    client.delete(reports_key)

    await message_to_delete.delete()
    await message.answer('Вердикт вынесен.')
    await send_recipe_to_check_reports(recipes, message, client)

    # warn user
    await UserWarn.create(admin=admin, user=user, reason=message.text, recipe=recipe)
    warnings = await UserWarn.filter(user=user).count()
    await message.bot.send_message(chat_id=user.tg_id,
                                   text=f'<b>⚠ ВАЖНО! ⚠</b>\n\n'
                                        f'<b>Уважаемый пользователь! {user.name}</b>\n'
                                        f'Администрация сделала предупреждение по рецепту, с связи с чем он был заморожен.\n'
                                        f'Ваш рецепт будет временно не доступен для поиска, добавления, просмотра '
                                        f'и прочих стандартных операций, до тех по пока Вы не измените его.\n'
                                        f'<b>{recipe.title}</b>\n'
                                        f'{recipe.url}')

    await message.bot.send_message(chat_id=user.tg_id,
                                   text=f'<b>⚠ ВАЖНО! ⚠</b>\n\n'
                                        f'Комментарии администрации:\n'
                                        f'<i>{message.text}<i>')

    if warnings == 3:
        user.is_active = False
        user.is_admin = False
        await message.bot.send_message(chat_id=user.tg_id,
                                       text=f'<b>⚠ ВАЖНО! ⚠</b>\n\n'
                                            f'<b>Уважаемый пользователь! {user.name}</b>\n'
                                            f'Вам было вынесено <b>3</b> предупреждения.'
                                            f'В связи с чем ваш акканут был заблокирован на нашей платформе на неограниченный срок.\n'
                                            f'Чтобы оспорить решение администрации обратитесь по этому адресу @GidroNn, указав номер своего аккаунта - <b>{user.tg_id}</b>'
                                            f'Надеемся на ваше понимание.\n'
                                            f'С уважением\n'
                                            f'Администрация бота.')
        await user.save()
    else:
        await message.bot.send_message(chat_id=user.tg_id,
                                       text=f'<b>⚠ ВАЖНО! ⚠</b>\n\n'
                                            f'На вашем аккаунте имеется {warnings} предупреждений.'
                                            f'Напоминаем, что если Вы получаете 3 предупреждения, то Ваш аккаунт будет заблокирован.\n'
                                            f'В случае если у вас возникли вопросы, обращайтесь по этому контакту - @GidroNn, указав номер свеого акканута - <b>user.tg_id</b>\n'
                                            f'Надеемся на ваше понимание.\n'
                                            f'С уважением\n'
                                            f'Администрация бота.')

    await state.clear()


@router.message(GetWarnReasonForm.reason, ~F.text)
async def invalid_getwarnreasonform(message: Message):
    await message.answer('Введите текст!')
