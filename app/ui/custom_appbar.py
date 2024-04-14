import flet as ft


class CustomAppBar(ft.AppBar):
    def __init__(self) -> None:
        super().__init__()
        self.toolbar_height = 75

        self.leading = ft.Icon()
        self.leading.name = ft.icons.DOWNLOAD

        self.title = ft.Text()
        self.title.value = 'Flet Tube'

        self.toggle_theme_button = ft.IconButton()
        self.toggle_theme_button.icon = ft.icons.LIGHT_MODE
        self.actions.append(self.toggle_theme_button)
