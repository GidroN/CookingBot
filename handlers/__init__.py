from aiogram import Router
from .admin import router as admin_handlers
from .user import router as user_handlers


router = Router(name='handlers')

router.include_routers(
    admin_handlers,
    user_handlers
)

__all__ = ('router', )
