from aiogram import Router
from bot.handlers import router as handler_router
from bot.callbacks import router as callback_router


router = Router(name='main')

router.include_routers(
    callback_router,
    handler_router,
)

__all__ = ('router', )
