from aiogram import Router
from .commands import router as admin_router
from .state_process import router as admin_state_router

router = Router(name='admin_handlers')

router.include_routers(
    admin_state_router,
    admin_router
)

__all__ = ('router', )
