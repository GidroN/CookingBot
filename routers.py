from aiogram import Router
from handlers import router as handler_router


router = Router(name='main')

router.include_routers(handler_router,)

__all__ = ('router', )