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
