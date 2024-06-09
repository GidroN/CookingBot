from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state, default_state
from aiogram.types import CallbackQuery, Message

from constants.callback import CallbackConstants
from database.models import Category, Recipe, Report, User, UserFavouriteRecipe
from database.redis_client import rc
from keyboards import (AddRecipeToFavouritesCallback, BackToType,
                       ChooseSearchTypeAction, DeleteRecipeAction,
                       PaginationCallback, PaginationKey, PaginationMarkup,
                       RecipeChangeItem, SearchType, UserChangeItem, cancel_mk,
                       cancel_or_skip_kb, confirm_delete_recipe,
                       search_by_category_panel, search_type_panel)
from keyboards.builders import (categories, single_recipe_panel,
                                user_recipe_panel)
from keyboards.factories import (BackCallback, ChangeRecipeInfoCallback,
                                 ChangeUserInfoCallback,
                                 ChooseSearchTypeByCategoryCallback,
                                 ChooseSearchTypeCallback,
                                 DeleteRecipeCallback, ReportRecipeCallback, UserAgreeAgreementCallback)
from misc.states import (AddRecipeForm, DeleteRecipeForm, EditRecipeForm,
                         EditUserForm, GetReportReasonForm, SearchRecipeForm, RegisterUserForm)
from misc.utils import (cache_list_update, check_recipe_in_favourites,
                        convert_ids_list_into_objects, get_list_from_cache,
                        get_main_kb, get_popular_recipes,
                        send_recipe_to_check_reports, send_report_reason,
                        send_user_recipe_change, send_user_recipe_info)

router = Router(name='user_callbacks')


@router.callback_query(AddRecipeForm.category, F.data.startswith('select_category_to_add_recipe_'))
async def choose_category_to_add_recipe(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]
    category = await Category.get(id=category_id)
    await callback.answer(f'Вы перешли в категорию {category.title}')
    await state.update_data(category=category)
    await state.set_state(AddRecipeForm.title)
    await callback.message.answer(f'Отлично, вы выбрали категорию <b>{category.title}</b>.\n'
                                  f'Теперь пришлите название рецепта.', reply_markup=cancel_mk)


@router.callback_query(SearchRecipeForm.search_type, ChooseSearchTypeCallback.filter())
async def choose_search_type(callback: CallbackQuery, callback_data: ChooseSearchTypeCallback, state: FSMContext):
    type = callback_data.type

    if type == SearchType.BY_CATEGORY:
        await callback.answer('Вы перешли к выбору категории.')
        await callback.message.edit_text('Выберите категорию, в которой хотите искать рецепт')
        await callback.message.edit_reply_markup(reply_markup=await categories('select_category_to_search_recipe_'))
        await state.set_state(SearchRecipeForm.category)
    elif type == SearchType.POPULAR:
        await callback.answer('Производится поиск по популярным рецептам.')
        await callback.message.delete()
        client = rc.get_client()
        ids = await get_popular_recipes().values_list('id', flat=True)
        key = f'{callback.message.chat.id}'
        cache_list_update(client, key, ids)
        result = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
        await send_user_recipe_info(result, callback.message)
        await state.clear()
    else:  # all
        await callback.answer('Производится поиск по всем рецептам.')
        await callback.message.edit_text('Выберите вариант поиска:')
        await callback.message.edit_reply_markup(reply_markup=search_by_category_panel('choose_search_type'))
        await state.set_state(SearchRecipeForm.ask_user_input)
        await state.update_data(message=callback.message, category=None)


@router.callback_query(any_state, BackCallback.filter(F.back_to_type == BackToType.CHOOSE_SEARCH_TYPE))
async def back_to_search_type(callback: CallbackQuery, callback_data: BackCallback, state: FSMContext):
    change_kb = callback_data.change_kb
    reply_markup = await search_type_panel()
    back_text = 'Вы вернулись к выбору варианту поиска.'
    choose_search_type_text = 'Выберите вариант поиска:'

    if change_kb:
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer(back_text, reply_markup=await get_main_kb(callback.message.from_user.id, True))
        await callback.message.answer(choose_search_type_text, reply_markup=reply_markup)
    else:
        await callback.answer(back_text)
        await callback.message.edit_text(choose_search_type_text)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)

    await state.set_state(SearchRecipeForm.search_type)


@router.callback_query(SearchRecipeForm.category, F.data.startswith('select_category_to_search_recipe_'))
async def choose_category_to_search_recipe(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]
    category = await Category.get(id=category_id)

    if await Recipe.filter(category=category).count() == 0:
        await callback.answer('В данной категорий пока что не опубликовано рецептов.', show_alert=True)
        return

    await callback.answer(f'Вы перешли в категорию {category.title}')
    await state.update_data(category=category)

    await callback.message.edit_text('Как хотите произвести поиск?')
    await callback.message.edit_reply_markup(reply_markup=search_by_category_panel('choose_category'))
    await state.update_data(message=callback.message)
    await state.set_state(SearchRecipeForm.ask_user_input)


@router.callback_query(any_state, BackCallback.filter(F.back_to_type == BackToType.CHOOSE_CATEGORY))
async def back_to_choose_category(callback: CallbackQuery, callback_data: BackCallback, state: FSMContext):
    await callback.answer('Вы вернулись к выбору категории.')
    await callback.message.edit_text('Выберите категорию в которой хотите искать рецепт:')
    await callback.message.edit_reply_markup(reply_markup=await categories('select_category_to_search_recipe_'))
    await state.set_state(SearchRecipeForm.category)


@router.callback_query(SearchRecipeForm.ask_user_input, ChooseSearchTypeByCategoryCallback.filter())
async def choose_search_type(callback: CallbackQuery, callback_data: ChooseSearchTypeByCategoryCallback, state: FSMContext):
    data = await state.get_data()
    category = data['category']
    message_to_delete = data['message']

    if callback_data.search_type == ChooseSearchTypeAction.SEARCH_BY_TITLE:
        await callback.answer('Вы выбрали поиск по названию.')
        await callback.message.answer('Введите название рецепта', reply_markup=cancel_mk)
        await state.update_data(search_type='name')

    elif callback_data.search_type == ChooseSearchTypeAction.SEARCH_BY_AUTHOR:
        await callback.answer(f'Вы выбрали поиск по автору')
        await callback.message.answer('Введите запрос', reply_markup=cancel_mk)
        await state.update_data(search_type='author')

    else:  # callback_data.search_type == ChooseSearchTypeAction.SEARCH_ALL
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id,
                                            action=ChatAction.TYPING)
        if category:  # all in category
            await callback.answer(f'Производится поиск по самым новым рецептам в категории {category.title}')
            client = rc.get_client()
            ids = await Recipe.filter(category=category, is_active=True).values_list('id', flat=True)
        else:  # all without category
            await callback.answer(f'Производится поиск по самым новым рецептам.')
            client = rc.get_client()
            ids = await Recipe.filter(is_active=True).values_list('id', flat=True)

        await message_to_delete.delete()
        key = f'{callback.message.chat.id}'
        cache_list_update(client, key, ids)
        result = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
        await send_user_recipe_info(result, callback.message, category, print_find=False)
        await state.clear()
        return

    await state.set_state(SearchRecipeForm.process_user_input)


@router.callback_query(default_state, PaginationCallback.filter())
async def process_search_result(callback: CallbackQuery, callback_data: PaginationCallback, state: FSMContext):
    client = rc.get_client()

    if callback_data.key == PaginationKey.DEFAULT:
        key = str(callback.from_user.id)
        model = Recipe
        prefetch_related = ['creator', 'category']
    else: # callback_data.key == Pagination.ADMIN_REPORT_CHECK
        key = f'{callback.from_user.id}!reports'
        model = Report
        prefetch_related = ['recipe', 'user']

    ids = get_list_from_cache(client, key, int)
    result = await convert_ids_list_into_objects(ids, model, prefetch_related)

    page = callback_data.page
    action = callback_data.action

    if action == 'prev':
        page -= 1
    elif action == 'next':
        page += 1

    if page < 0:
        page = 0
        await callback.answer('Это первая запись.')
    elif page >= len(result):
        page = len(result) - 1
        await callback.answer('Это последняя запись.')

    if callback_data.markup == PaginationMarkup.VIEWER:
        await send_user_recipe_info(result, callback.message, page=page, print_find=False, edit_msg=True)
    elif callback_data.markup == PaginationMarkup.ADMIN_RECIPE:
        await send_recipe_to_check_reports(result, callback.message, client, page=page, edit_msg=True)
    elif callback_data.markup == PaginationMarkup.ADMIN_REPORT:
        await send_report_reason(result, callback.message, page=page, edit_msg=True)
    else:
        await send_user_recipe_change(result, callback.message, page=page, edit_msg=True)


@router.callback_query(default_state, AddRecipeToFavouritesCallback.filter())
async def process_add_to_favourites(callback: CallbackQuery, callback_data: AddRecipeToFavouritesCallback,
                                    state: FSMContext):
    recipe_id = callback_data.recipe_id
    page = callback_data.page
    single_recipe_view = callback_data.single_recipe_view
    user_tg_id = callback.from_user.id

    recipe = await Recipe.get(id=recipe_id)
    user = await User.get(tg_id=user_tg_id)
    favourited_by_user = await check_recipe_in_favourites(recipe.id, user_tg_id)

    if favourited_by_user:
        reply_markup = user_recipe_panel(recipe.id, False, page)
        await UserFavouriteRecipe.filter(recipe=recipe, user=user).delete()
        await callback.answer('Удален из сохраненных.')

        if single_recipe_view:
            reply_markup = single_recipe_panel(recipe.id, False)

        await callback.message.edit_reply_markup(reply_markup=reply_markup)
    else:
        await UserFavouriteRecipe.create(recipe=recipe, user=user)
        await callback.answer('Добавлен в сохраненные.')
        reply_markup = user_recipe_panel(recipe.id, True, page)

        if single_recipe_view:
            reply_markup = single_recipe_panel(recipe.id, True)

        await callback.message.edit_reply_markup(reply_markup=reply_markup)


@router.callback_query(default_state, ReportRecipeCallback.filter())
async def process_user_recipe_report(callback: CallbackQuery, callback_data: ReportRecipeCallback, state: FSMContext):
    recipe_id = callback_data.recipe_id
    user_id = callback.message.chat.id

    recipe = await Recipe.get(id=recipe_id)
    user = await User.get(tg_id=user_id)

    if await Report.filter(recipe=recipe, user=user).exists():
        await callback.answer('Вы уже отправляли жалобу ранее на этот рецепт.', show_alert=True)
    else:
        await callback.answer()
        await callback.message.answer('Опишите пожалуйста причину жалобы', reply_markup=cancel_or_skip_kb)
        await state.update_data(user=user, recipe=recipe)
        await state.set_state(GetReportReasonForm.reason)


@router.callback_query(default_state, ChangeRecipeInfoCallback.filter())
async def process_change_recipe_info(callback: CallbackQuery, callback_data: ChangeRecipeInfoCallback,
                                     state: FSMContext):
    await callback.answer()

    change_item = callback_data.change_item
    recipe_id = callback_data.recipe_id

    if change_item == RecipeChangeItem.NAME:
        await callback.message.answer('Введите новое название для рецепта', reply_markup=cancel_mk)
        await state.set_state(EditRecipeForm.get_user_input)

    elif change_item == RecipeChangeItem.LINK:
        await callback.message.answer('Введите новую ссылку на рецепт:', reply_markup=cancel_mk)
        await state.set_state(EditRecipeForm.get_user_input)

    elif change_item == RecipeChangeItem.CATEGORY:
        await callback.message.answer('Выберите категорию:', reply_markup=await categories('recipe_edit_category_', False, True))
        await state.set_state(EditRecipeForm.category)

    else: # delete
        await callback.message.answer('Вы уверены, что хотите удалить этот рецепт?', reply_markup=confirm_delete_recipe)
        await state.set_state(DeleteRecipeForm.confirm)
        await state.update_data(recipe_id=recipe_id, message=callback.message)

    await state.update_data(change_item=change_item, recipe_id=recipe_id)


@router.callback_query(DeleteRecipeForm.confirm, DeleteRecipeCallback.filter())
async def process_delete_recipe_form(callback: CallbackQuery, callback_data: DeleteRecipeCallback, state: FSMContext):
    action = callback_data.action
    data = await state.get_data()
    recipe_id = data['recipe_id']
    message_to_edit = data['message']
    recipe = await Recipe.get(id=recipe_id)

    if action == DeleteRecipeAction.CANCEL:
        await callback.message.delete()
        await callback.answer('Отменено.')
    else:  # action == CONFIRM
        await recipe.delete()
        await callback.message.delete()
        await callback.answer('Рецепт успешно удален!')

        client = rc.get_client()
        key = f'{callback.message.chat.id}'
        ids = get_list_from_cache(client, key, int)
        ids.remove(recipe_id)
        cache_list_update(client, key, ids)
        recipes = await convert_ids_list_into_objects(ids, Recipe, ['category', 'creator'])
        await send_user_recipe_info(recipes, message_to_edit, print_find=False, edit_msg=True)

    await state.clear()


@router.callback_query(EditRecipeForm.category, F.data.startswith('recipe_edit_category'))
async def process_recipe_edit_category(callback: CallbackQuery, state: FSMContext):
    recipe_id = (await state.get_data())['recipe_id']
    last_char = callback.data.split('_')[-1]

    if not last_char.isdigit():
        await callback.message.delete()
        await state.set_state(default_state)
        return

    category_id = int(last_char)

    category = await Category.get(id=category_id)
    recipe = await Recipe.get(id=recipe_id)

    recipe.category = category
    await recipe.save()

    await callback.answer('Категория успешно изменена.')
    await callback.message.delete()

    await state.clear()


@router.callback_query(ChangeUserInfoCallback.filter())
async def change_user_info(callback: CallbackQuery, callback_data: ChangeUserInfoCallback, state: FSMContext):
    change_item = callback_data.change_item
    tg_id = callback_data.tg_id
    user = await User.get(tg_id=tg_id)

    if change_item == UserChangeItem.NAME:
        await callback.message.answer('Введите новое имя:',
                                      reply_markup=cancel_mk)

    await state.set_state(EditUserForm.get_user_input)
    await state.update_data(user=user, change_item=change_item)
