from enum import StrEnum


class ButtonText(StrEnum):
    MAIN_MENU = '🏠 Главное меню'
    SEARCH_RECIPES = '🔎 Искать рецепт'
    FAVOURITE_RECIPES = '♥ Избранное'
    ADD_TO_FAVOURITE_RECIPES = '♥ Добавить в избранное'
    ADDED_TO_FAVOURITE_RECIPES = '✔ Добавить в избранное'
    REPORT_RECIPE = '⚠ Пожаловаться'
    MY_RECIPES = '📚 Мои рецепты'
    ADD_RECIPE = '➕ Добавить рецепт'
    PROFILE = '⚙ Профиль'
    TIMER = '⏱ Таймер'
    CANCEL = '❌ Отменить'
    CONFIRM = '✔ Принять'
    SEARCH_ALL_RECIPES = '🛒 Все рецепты'
    SEARCH_BY_TITLE = '✏ Поиск по названию'
    SEARCH_BY_AUTHOR = '👤 Поиск по автору'
    PREV = '⬅ Назад'
    NEXT = '➡ Вперед'
    CHANGE_RECIPE_NAME = '✏ Изменить название'
    CHANGE_RECIPE_URL = '✏ Изменить ссылку'
    DELETE_RECIPE = '🗑 Удалить рецепт'
