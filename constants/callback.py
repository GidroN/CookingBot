from enum import StrEnum


class CallbackConstants(StrEnum):
    DELETE_MESSAGE = 'delete_message'
    AGREE_AGREEMENT = 'agree_agreement'
    EDIT_CATEGORY = 'edit_category'
    CHOOSE_CATEGORY_TO_CHANGE = 'choose_category_to_change'
    ADD_CATEGORY = 'add_category'
