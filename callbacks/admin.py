from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from constants.factory import BackToType, CategoryChangeItem, DeleteAction
from database.models import Recipe, Report, Category
from database.redis_client import rc
from keyboards import (CheckReportsCallback, FalseAlarmRecipeCallback,
                       WarnUserCallback, cancel_mk, category_change_panel, BackCallback, categories,
                       ChangeCategoryInfoCallback, confirm_delete_recipe, DeleteItemCallback)
from constants.callback import CallbackConstants as Cb, CallbackConstants
from misc.states import GetWarnReasonForm, EditCategoryForm, AddCategoryForm, DeleteCategoryForm
from misc.utils import (cache_list_update, convert_ids_list_into_objects,
                        get_list_from_cache, send_recipe_to_check_reports,
                        send_report_reason, get_main_kb)

router = Router(name='admin_callbacks')


@router.callback_query(CheckReportsCallback.filter())
async def process_check_reports_callback(callback: CallbackQuery, callback_data: CheckReportsCallback):
    recipe_id = callback_data.recipe_id

    client = rc.get_client()
    client.set(f'{callback.from_user.id}:current_recipe_id', recipe_id)
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

    await callback.message.answer('Вердикт вынесен.')

    if ids:
        cache_list_update(client, key, ids)
        recipes = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
        client.delete(reports_key)
        await send_recipe_to_check_reports(recipes, callback.message, client, edit_msg=True)
    else:
        await callback.message.delete()
        await callback.answer('Вы просмотрели все жалобы.', show_alert=True)


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

    if not recipe.is_active:
        key = str(callback.from_user.id)
        await callback.answer('Данный рецепт уже был обработан.', show_alert=True)
        ids = get_list_from_cache(client, key, int)
        if ids:
            ids.remove(recipe_id)
            cache_list_update(client, key, ids)
            recipes = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
            client.delete(reports_key)
            await send_recipe_to_check_reports(recipes, callback.message, client, edit_msg=True)
        else:
            await callback.message.answer('На текущий момент нет рецептов с жалобами.')
        return

    await callback.answer()
    await callback.message.answer('Введите пожалуйста причину предупреждения:', reply_markup=cancel_mk)
    await state.set_state(GetWarnReasonForm.reason)
    await state.update_data(user=user, recipe=recipe, message=callback.message)


@router.callback_query(F.data == CallbackConstants.ADD_CATEGORY)
async def add_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите имя для категории:', reply_markup=cancel_mk)
    await state.set_state(AddCategoryForm.get_user_input)


@router.callback_query(F.data == CallbackConstants.EDIT_CATEGORY)
@router.callback_query(BackCallback.filter(F.back_to_type == BackToType.CHOOSE_CATEGORY_EDIT))
async def select_option_edit_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы вернулись к выбору категории')
    await callback.message.edit_text('Выберите категорию для изменения:')
    await callback.message.edit_reply_markup(reply_markup=await categories(CallbackConstants.CHOOSE_CATEGORY_TO_CHANGE + '_', prev=False))
    await state.set_state(EditCategoryForm.choose_category)


@router.callback_query(EditCategoryForm.choose_category, F.data.startswith(CallbackConstants.CHOOSE_CATEGORY_TO_CHANGE))
async def choose_category_to_change(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split('_')[-1])
    category = await Category.get(id=category_id)
    await callback.answer(f'Вы перешли в категорию {category.title}')
    await callback.message.edit_text(f'Категория: {category.title}')
    await callback.message.edit_reply_markup(reply_markup=category_change_panel(category_id))
    await state.update_data(category=category)


@router.callback_query(ChangeCategoryInfoCallback.filter())
async def select_option_to_change_category(callback: CallbackQuery, callback_data: ChangeCategoryInfoCallback, state: FSMContext):
    change_item = callback_data.change_item
    category = (await state.get_data())['category']
    recipes = await Recipe.filter(category=category).count()

    if change_item == CategoryChangeItem.TITLE:
        await callback.answer()
        await callback.message.answer('Введите пожалуйста новое название:', reply_markup=cancel_mk)
        await state.set_state(EditCategoryForm.get_user_input)
    else: # change_item = CategoryChangeItem.DELETE
        if not recipes:
            await callback.answer()
            await callback.message.answer('Вы уверены, что хотите удалить эту категорию?',
                                          reply_markup=confirm_delete_recipe)
            await state.set_state(DeleteCategoryForm.confirm)
            await state.update_data(message=callback.message)
        else:
            await callback.answer(f'На данный момент в этой категории создано {recipes} рецептов, и вы не сможете ее удалить.', True)
            await state.clear()


@router.callback_query(DeleteCategoryForm.confirm, DeleteItemCallback.filter())
async def delete_category(callback: CallbackQuery, callback_data: DeleteItemCallback, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    category = data['category']
    message_to_delete = data['message']
    action = callback_data.action

    if action == DeleteAction.CONFIRM:
        await category.delete()
        await callback.message.answer('Категория успешно удалена.')
        await message_to_delete.delete()

    await callback.message.delete()
    await state.clear()
