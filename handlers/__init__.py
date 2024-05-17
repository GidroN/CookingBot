from aiogram import Router
from .state_process import router as state_router
from .user import router as user_router
from .admin import router as admin_router


router = Router()

router.include_routers(
    state_router,
    admin_router,
    user_router,
)

__all__ = ('router', )
