from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, any_state
from aiogram.types import Message, CallbackQuery

from database.models import Category, Recipe, User, UserFavouriteRecipe, Report
from database.redis_client import rc
from keyboards import (cancel_mk, RecipePaginationCallback,
                       AddRecipeToFavouritesCallback, PaginationMarkup, RecipeChangeItem,
                       confirm_delete_recipe, DeleteRecipeAction, search_by_category_panel, SearchType, BackToType,
                       search_type_panel)
from keyboards.builders import categories, user_recipe_panel, single_recipe_panel
from keyboards.button_text import ButtonText as BT
from keyboards.factories import ReportRecipeCallback, ChangeRecipeInfoCallback, DeleteRecipeCallback, \
    BackCallback, ChooseSearchTypeCallback
from misc.states import AddRecipeForm, SearchRecipeForm, EditRecipeForm, DeleteRecipeForm
from misc.utils import check_recipe_in_favourites, get_main_kb, send_user_recipe_info, get_list_from_cache, convert_ids_list_into_objects, \
    cache_list_update, send_user_recipe_change

router = Router(name='user_callbacks')


@router.message(F.text == BT.MAIN_MENU)
@router.message(Command('menu'))
async def menu(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    await state.clear()
    await message.answer('🏠 Вы перешли в главное меню', reply_markup=get_main_kb(tg_id))


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
        ...
        # client = rc.get_client()
        # ids = await Recipe.all().prefetch_related('category', 'creator').values_list('id', flat=True)
        # key = f'{callback.message.chat.id}'
        # cache_list_update(client, key, ids)
        # result = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
        # await send_user_recipe_info(result, callback.message)
        # await state.clear()
    else: # all
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
        await callback.message.answer(back_text, reply_markup=get_main_kb(callback.message.from_user.id, True))
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


@router.callback_query(SearchRecipeForm.ask_user_input, F.data.startswith('choose_search_type_by_'))
async def choose_search_type(callback: CallbackQuery, state: FSMContext):
    search_type = callback.data.split('_')[-1]
    data = await state.get_data()
    category = data['category']
    message_to_delete = data['message']

    if search_type == 'name':
        await callback.answer('Вы выбрали поиск по названию.')
        await callback.message.answer('Введите название рецепта', reply_markup=cancel_mk)

    elif search_type == 'author':
        await callback.answer(f'Вы выбрали поиск по автору')
        await callback.message.answer('Введите запрос', reply_markup=cancel_mk)

    elif search_type == 'all':
        if category: # all in category
            await callback.answer(f'Производится поиск по самым новым рецептам в категории {category.title}')
            client = rc.get_client()
            ids = await Recipe.filter(category=category).values_list('id', flat=True)
        else: # all without category
            await callback.answer(f'Производится поиск по самым новым рецептам.')
            client = rc.get_client()
            ids = await Recipe.all().values_list('id', flat=True)

        await message_to_delete.delete()
        key = f'{callback.message.chat.id}'
        cache_list_update(client, key, ids)
        result = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
        await send_user_recipe_info(result, callback.message, category, print_find=False)
        await state.clear()
        return

    await state.set_state(SearchRecipeForm.process_user_input)
    await state.update_data(search_type=search_type)


@router.callback_query(default_state, RecipePaginationCallback.filter())
async def process_search_result(callback: CallbackQuery, callback_data: RecipePaginationCallback, state: FSMContext):
    client = rc.get_client()
    key = f'{callback.message.chat.id}'
    ids = get_list_from_cache(client, key, int)
    result = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])

    page = callback_data.page
    action = callback_data.action

    if action == 'prev':
        page -= 1
    if action == 'next':
        page += 1

    if page < 0:
        page = 0
        await callback.answer('Это первый рецепт.')
    if page >= len(result):
        page = len(result) - 1
        await callback.answer('Это последний рецепт.')

    if callback_data.markup == PaginationMarkup.VIEWER:
        await send_user_recipe_info(result, callback.message, page=page, print_find=False, edit_msg=True)
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
        reply_markup = user_recipe_panel(recipe.id, False, page)

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
        await Report.create(recipe=recipe, user=user)
        await callback.answer('Ваша жалоба записана!', show_alert=True)

        reports_quantity = await Report.filter(recipe=recipe).count()

        if reports_quantity >= 3:
            # TODO: Notify admins
            ...


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
        await callback.message.answer('Выберите категорию:', reply_markup=await categories('recipe_edit_category_'))
        await state.set_state(EditRecipeForm.category)

    else:
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
    category_id = int(callback.data.split('_')[-1])

    category = await Category.get(id=category_id)
    recipe = await Recipe.get(id=recipe_id)

    recipe.category = category
    await recipe.save()

    await callback.answer('Категория успешно изменена.')
    await callback.message.delete()

    await state.clear()

