from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database.models import Category, Recipe, User, UserFavouriteRecipe, Report
from database.redis_client import rc
from keyboards import cancel_mk, search_type_panel, RecipePaginationCallback, \
    AddRecipeToFavouritesCallback, PaginationMarkup, RecipeChangeItem, confirm_delete_recipe, DeleteRecipeAction
from keyboards.builders import categories, user_recipe_panel
from keyboards.button_text import ButtonText as BT
from keyboards.factories import ReportRecipeCallback, ChangeRecipeInfoCallback, DeleteRecipeCallback
from misc.states import AddRecipeForm, SearchRecipeForm, EditRecipeForm, DeleteRecipeForm
from misc.utils import get_main_kb, send_user_recipe_info, get_list_from_cache, convert_ids_list_into_objects, \
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
                                  f'Теперь пришлите название рецепта.')
    # await callback.message.answer(f'Отлично, вы выбрали категорию <b>{category.title}</b>.\n'
    #                               f'Теперь чтобы добавить рецепт, заполните информацию в таком виде (Пробелы после скобок соблюдать!):\n'
    #                               f'---------------------------------------------\n'
    #                               f'1) Название\n'
    #                               f'2) Ссылка на статью с рецептом в https://telegra.ph \n'
    #                               f'---------------------------------------------\n'
    #                               f'Подробнее про телеграф - https://uchet-jkh.ru/i/telegraf-dlya-telegram-cto-eto-i-kak-ono-rabotaet/',
    #                               reply_markup=cancel_mk)


@router.callback_query(SearchRecipeForm.category, F.data.startswith('select_category_to_search_recipe_'))
async def choose_category_to_search_recipe(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]

    if category_id.isdigit():
        category = await Category.get(id=category_id)
        await callback.answer(f'Вы перешли в категорию {category.title}')
        await state.update_data(category=category)
    else:  # all
        await callback.answer('Производиться поиск по всем рецептам.')
        await state.update_data(search_type='all', category=None)

    await callback.message.edit_text('Как хотите произвести поиск?')
    await callback.message.edit_reply_markup(reply_markup=search_type_panel)
    await state.set_state(SearchRecipeForm.search_type)


@router.callback_query(SearchRecipeForm.search_type, F.data == 'back_to_choose_category')
async def back_to_choose_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы вернулись к выбору категории.')
    await callback.message.edit_text('Выберите категорию в которой хотите искать рецепт:')
    await callback.message.edit_reply_markup(
        reply_markup=await categories('select_category_to_search_recipe_', show_all_recipes=True))
    await state.set_state(SearchRecipeForm.category)


@router.callback_query(SearchRecipeForm.search_type, F.data.startswith('choose_search_type_by_'))
async def choose_search_type(callback: CallbackQuery, state: FSMContext, bot: Bot):
    search_type = callback.data.split('_')[-1]
    category = (await state.get_data())['category']

    if search_type == 'name':
        await callback.answer(f'Вы выбрали поиск по названию.')
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

        key = str(callback.message.chat.id)
        cache_list_update(client, key, ids)
        result = await convert_ids_list_into_objects(ids, Recipe, ['creator', 'category'])
        await send_user_recipe_info(result, callback.message, category)
        await state.clear()
        return

    await state.set_state(SearchRecipeForm.get_user_input)
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
    user = await User.get(tg_id=callback.message.chat.id).prefetch_related('favourite_recipes')
    favourite = await user.favourite_recipes.all()
    recipe = await Recipe.get(id=recipe_id)
    if recipe in favourite:
        await UserFavouriteRecipe.filter(recipe=recipe, user=user).delete()
        await callback.answer('Удален из сохраненных.')
        await callback.message.edit_reply_markup(reply_markup=user_recipe_panel(recipe.id, False, page))
    else:
        await UserFavouriteRecipe.create(recipe=recipe, user=user)
        await callback.answer('Добавлен в сохраненные.')
        await callback.message.edit_reply_markup(reply_markup=user_recipe_panel(recipe.id, True, page))


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
        await state.update_data(recipe_id=recipe_id)

    await state.update_data(change_item=change_item, recipe_id=recipe_id)


@router.callback_query(DeleteRecipeForm.confirm, DeleteRecipeCallback.filter())
async def process_delete_recipe_form(callback: CallbackQuery, callback_data: DeleteRecipeCallback, state: FSMContext):
    action = callback_data.action
    recipe_id = (await state.get_data())['recipe_id']
    recipe = await Recipe.get(id=recipe_id)

    if action == DeleteRecipeAction.CANCEL:
        await callback.message.delete()
        await callback.answer('Отменено.')
    else:  # action == CONFIRM
        await recipe.delete()
        await callback.message.delete()
        await callback.message.answer('Рецепт успешно удален!')

        client = rc.get_client()
        key = f'{callback.message.chat.id}'
        ids = get_list_from_cache(client, key, int)
        ids.remove(recipe_id)
        cache_list_update(client, key, ids)

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
