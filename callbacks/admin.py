from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.models import Report, Recipe
from database.redis_client import rc
from keyboards import CheckReportsCallback, FalseAlarmRecipeCallback, WarnUserCallback, cancel_mk
from keyboards.callback_constants import CallbackConstants as Cb
from misc.states import GetWarnReasonForm
from misc.utils import get_list_from_cache, convert_ids_list_into_objects, send_report_reason, \
    send_recipe_to_check_reports, cache_list_update

router = Router(name='admin_callbacks')


@router.callback_query(CheckReportsCallback.filter())
async def process_check_reports_callback(callback: CallbackQuery, callback_data: CheckReportsCallback):
    recipe_id = callback_data.recipe_id

    client = rc.get_client()
    key = f'{callback.from_user.id}!{recipe_id}!reports'
    report_ids = await Report.filter(recipe__id=recipe_id).values_list('id', flat=True)

    cache_list_update(client, key, report_ids)
    ids = get_list_from_cache(client, key, int)
    reports = await convert_ids_list_into_objects(ids, Report, ['recipe', 'user'])

    await callback.answer()
    await send_report_reason(reports, callback.message)


@router.callback_query(F.data == Cb.DELETE_MESSAGE)
async def process_close_report_windows(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(FalseAlarmRecipeCallback.filter())
async def process_false_alarm(callback: CallbackQuery, callback_data: FalseAlarmRecipeCallback):
    client = rc.get_client()
    recipe_id = callback_data.recipe_id
    reports_key = f'{callback.from_user.id}!{recipe_id}!reports'

    if not client.exists(reports_key):
        await callback.answer('Прежде чем вынести вердикт, пожалуйста ознакомьтесь с жалобами.', show_alert=True)
        return

    key = str(callback.from_user.id)
    qs = await Report.filter(recipe__id=recipe_id)

    for obj in qs:
        await obj.delete()

    ids = get_list_from_cache(client, key, int)
    ids.remove(recipe_id)
    cache_list_update(client, key, ids)
    recipes = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
    client.delete(reports_key)
    await callback.answer('Вердикт вынесен.')
    await send_recipe_to_check_reports(recipes, callback.message, client, edit_msg=True)


@router.callback_query(WarnUserCallback.filter())
async def warn_user(callback: CallbackQuery, callback_data: WarnUserCallback, state: FSMContext):
    recipe_id = callback_data.recipe_id
    recipe = await Recipe.get(id=recipe_id).prefetch_related('creator', 'category')
    user = recipe.creator
    client = rc.get_client()

    reports_key = f'{callback.from_user.id}!{recipe_id}!reports'

    if not client.exists(reports_key):
        await callback.answer('Прежде чем вынести вердикт, пожалуйста ознакомьтесь с жалобами.', show_alert=True)
        return

    await callback.answer()
    await callback.message.answer('Введите пожалуйста причину предупреждения:', reply_markup=cancel_mk)
    await state.set_state(GetWarnReasonForm.reason)
    await state.update_data(user=user, recipe=recipe, message=callback.message)
