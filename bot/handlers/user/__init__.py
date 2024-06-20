from aiogram import Router
from .commands import router as user_router
from .state_process import router as user_state_router

router = Router(name='user_handlers')

router.include_routers(
    user_state_router,
    user_router
)

__all__ = ('router', )
