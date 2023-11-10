from typing import Optional

import flet as ft
from flet_core import AppBar

from app.ui import CustomAppBar


class BaseView(ft.View):
    def __init__(self) -> None:
        super().__init__()
        self.appbar = CustomAppBar()

    @ft.View.appbar.getter
    def appbar(self) -> AppBar:
        return super().appbar
