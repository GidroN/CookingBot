from enum import StrEnum


class ButtonText(StrEnum):
    REGISTER = '👤 Пройти регистрацию'
    READ_AGREEMENT = '📕 Прочесть лицензионное соглашение'
    AGREE_AGREEMENT = '✅ Я согласен с условиями'
    MAIN_MENU = '🏠 Главное меню'
    SEARCH_RECIPES = '🔎 Искать рецепт'
    FAVOURITE_RECIPES = '♥ Избранное'
    ADD_TO_FAVOURITE_RECIPES = '♥ Добавить в избранное'
    ADDED_TO_FAVOURITE_RECIPES = '✔ Добавить в избранное'
    RANDOM_RECIPE = '🎲 Случайный рецепт'
    REPORT_RECIPE = '⚠ Пожаловаться'
    MY_RECIPES = '📚 Мои рецепты'
    ADD_RECIPE = '➕ Добавить рецепт'
    PROFILE = '⚙ Профиль'
    TIMER = '⏱ Таймер'
    CANCEL = '❌ Отменить'
    CONFIRM = '✔ Принять'
    DELAY = '🕰 Отложить'
    SEARCH_ALL_RECIPES = '🛒 Все рецепты'
    SEARCH_ALL_CATEGORY = '🍽 Все категории'
    SEARCH_BY_TITLE = '✏ Поиск по названию'
    SEARCH_BY_AUTHOR = '👤 Поиск по автору'
    SEARCH_REPEAT = '🔎 Повторный поиск'
    SEARCH_POPULAR = '🔥 Популярное'
    SEARCH_BY_CATEGORY = '🍴 По категориям'
    PREV = '⬅ Назад'
    NEXT = '➡ Вперед'
    SKIP = '➡ Пропустить'
    CHANGE_RECIPE_NAME = '✏ Изменить название'
    CHANGE_RECIPE_URL = '✏ Изменить ссылку'
    CHANGE_RECIPE_CATEGORY = '✏ Изменить категорию'
    DELETE_RECIPE = '🗑 Удалить рецепт'
    CHECK_REPORTS = '👁 Просмотреть жалобы'
    ADMIN_INTERFACE = '🕵️‍♂️ Интерфейс администратора'
    USER_INTERFACE = '🧑 Интерфейс пользователя'
    ADMIN_PANEL = '🛠 Административная панель'
    GET_RECIPE_BY_ID = '🛠 Управлять рецептом'
    GET_USER_BY_ID = '🛠 Управлять пользователем'
    CLOSE = '❌ Закрыть'
    FALSE_ALARM = '✔ Нарушений не выявлено'
    WARN_USER = '⚠ Сделать предупреждение'
    DEATH = '💀'
    CHANGE_USER_NAME = '✏ Изменить имя'
    # DELETE_PROFILE = '🗑 Удалить профиль'
    MANAGE_CATEGORIES = '🍴 Управлять категориями'
    CHANGE_CATEGORY = '✏ Изменить категорию'
    CHANGE_CATEGORY_TITLE = '✏ Изменить имя'
    DELETE_CATEGORY = '🗑 Удалить категорию'
    ADD_CATEGORY = '➕ Добавить категорию'