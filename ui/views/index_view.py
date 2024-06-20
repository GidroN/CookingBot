import flet as ft
from flet_route import Params, Basket


class IndexView:
    def __init__(self):
        ...

    async def view(self, page: ft.page, params: Params, basket: Basket):
        self.page = page
        print(params)
        print(basket)

        return ft.View(
            "/",
            controls=[
                ft.Text("This Is Index View"),
                ft.ElevatedButton("Go Next View", on_click=lambda _: self.page.go("/next_view/10")),
            ]
        )
