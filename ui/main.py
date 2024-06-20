import flet as ft
from flet_route import Routing
from routes import app_routes
from middlewares.app_middleware import AppBasedMiddleware


async def main(page: ft.Page):
    Routing(
        page=page,
        app_routes=app_routes,
        middleware=AppBasedMiddleware().call_me,
        async_is=True
    )
    page.go(page.route)


ft.app(target=main)
