import flet as ft

from app.ui import SuccessBanner


class DangerBanner(SuccessBanner):
    def __init__(self) -> None:
        super().__init__()
        self.icon.name = ft.icons.DANGEROUS
        self.bgcolor = ft.colors.RED
