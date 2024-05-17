from aiogram import Router
from handlers import router as handler_router
from callbacks import router as callback_router


router = Router(name='main')

router.include_routers(
    callback_router,
    handler_router,
)

__all__ = ('router', )
