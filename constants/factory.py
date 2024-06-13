from enum import StrEnum


class PaginationAction(StrEnum):
    PREV = 'prev'
    NEXT = 'next'


class PaginationMarkup(StrEnum):
    VIEWER = 'viewer'
    OWNER = 'owner'
    ADMIN_RECIPE = 'admin_recipe' # as report recipe view
    ADMIN_REPORT = 'admin_report'


class PaginationKey(StrEnum):
    DEFAULT = '{message.from_user.id}'
    ADMIN_REPORT_CHECK = '{message.from_user.id}!report'


class RecipeChangeItem(StrEnum):
    NAME = 'name'
    LINK = 'link'
    CATEGORY = 'category'
    DELETE = 'delete'


class DeleteAction(StrEnum):
    CONFIRM = 'confirm'
    CANCEL = 'cancel'


class SearchType(StrEnum):
    POPULAR = 'popular'
    ALL_RECIPES = 'all'
    BY_CATEGORY = 'by_category'


class BackToType(StrEnum):
    CHOOSE_CATEGORY = 'category'
    CHOOSE_SEARCH_TYPE = 'search_type'
    CHOOSE_CATEGORY_EDIT = 'category_edit'


class ChooseSearchTypeAction(StrEnum):
    SEARCH_BY_TITLE = 'title'
    SEARCH_BY_AUTHOR = 'author'
    SEARCH_ALL = 'all'


class UserChangeItem(StrEnum):
    NAME = 'name'


class CategoryChangeItem(StrEnum):
    TITLE = 'title'
    DELETE = 'delete'


# class DeleteCategoryAction(StrEnum):
#     CONFIRM = 'confirm'
#     CANCEL = 'cancel'
