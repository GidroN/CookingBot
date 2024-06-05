from enum import StrEnum


class PaginationAction(StrEnum):
    PREV = 'prev'
    NEXT = 'next'


class PaginationMarkup(StrEnum):
    VIEWER = 'viewer'
    OWNER = 'owner'


class RecipeChangeItem(StrEnum):
    NAME = 'name'
    LINK = 'link'
    CATEGORY = 'category'
    DELETE = 'delete'


class DeleteRecipeAction(StrEnum):
    CONFIRM = 'confirm'
    CANCEL = 'cancel'


class SearchType(StrEnum):
    POPULAR = 'popular'
    ALL_RECIPES = 'all'
    BY_CATEGORY = 'by_category'


class BackToType(StrEnum):
    CHOOSE_CATEGORY = 'category'
    CHOOSE_SEARCH_TYPE = 'search_type'


class ChooseSearchTypeAction(StrEnum):
    SEARCH_BY_TITLE = 'title'
    SEARCH_BY_AUTHOR = 'author'
    SEARCH_ALL = 'all'
