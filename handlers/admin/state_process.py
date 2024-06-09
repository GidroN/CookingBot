from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.models import Recipe, User, UserWarn, Report
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

    # recipe.is_active = False
    # await recipe.save()

    # delete reports
    qs = await Report.filter(recipe=recipe)
    for obj in qs:
        await obj.delete()

    # warn user
    await UserWarn.create(admin=admin, user=user, reason=message.text, recipe=recipe)
    warnings = await UserWarn.filter(user=user).count()
    await message.bot.send_message(chat_id=user.tg_id,
                                   text=f'<b>⚠ ВАЖНО! ⚠</b>\n\n'
                                        f'<b>Уважаемый пользователь! {user.name}</b>\n'
                                        f'Администрация сделала предупреждение по рецепту, с связи с чем он был заморожен.\n'
                                        f'Ваш рецепт теперь не доступен для поиска, добавления, просмотра и прочих стандартных операций.\n\n'
                                        f'<b>{recipe.title}</b>\n'
                                        f'{recipe.url}')

    await message.bot.send_message(chat_id=user.tg_id,
                                   text=f'<b>⚠ ВАЖНО! ⚠</b>\n\n'
                                        f'Комментарии администрации:\n'
                                        f'<i>{message.text}</i>')

    if warnings == 3:
        user.is_active = False
        user.is_admin = False
        await message.bot.send_message(chat_id=user.tg_id,
                                       text=f'<b>⚠ ВАЖНО! ⚠</b>\n\n'
                                            f'<b>Уважаемый пользователь! {user.name}</b>\n'
                                            f'Вам было вынесено <b>3</b> предупреждения.'
                                            f'В связи с чем ваш акканут был заблокирован на нашей платформе на неограниченный срок.\n'
                                            f'Надеемся на ваше понимание.\n'
                                            f'С уважением\n'
                                            f'Администрация бота.')
        await user.save()
    else:
        await message.bot.send_message(chat_id=user.tg_id,
                                       text=f'<b>⚠ ВАЖНО! ⚠</b>\n\n'
                                            f'На вашем аккаунте имеется {warnings} предупреждений.'
                                            f'Напоминаем, что если Вы получаете 3 предупреждения,'
                                            f' то Ваш аккаунт будет заблокирован.\n'
                                            f'Надеемся на ваше понимание.\n'
                                            f'С уважением,\n'
                                            f'Администрация бота.')

    # redis updating cache
    reports_key = f'{message.from_user.id}!{recipe.id}!reports'
    key = str(message.from_user.id)

    ids = get_list_from_cache(client, key, int)
    ids.remove(recipe.id)
    await message_to_delete.delete()
    await message.answer('Вердикт вынесен.', reply_markup=await get_main_kb(admin.tg_id, show_admin_panel=True))

    if ids:
        cache_list_update(client, key, ids)
        recipes = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
        client.delete(reports_key)
        await send_recipe_to_check_reports(recipes, message, client)
    else:
        await message.answer('Вы просмотрели все жалобы.')

    await state.clear()


@router.message(GetWarnReasonForm.reason, ~F.text)
async def invalid_getwarnreasonform(message: Message):
    await message.answer('Введите текст!')
