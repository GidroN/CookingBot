from aiogram import Router
from .user import router as user_router
from .admin import router as admin_router

router = Router(name='callbacks')

router.include_routers(
    # callback_factories,
    admin_router,
    user_router,
)

__all__ = ('router', )
