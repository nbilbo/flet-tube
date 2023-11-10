import flet as ft


class CustomAppBar(ft.AppBar):
    def __init__(self) -> None:
        super().__init__()
        self.bgcolor = '#592F25'
        self.toolbar_height = 75

        self.leading = ft.Image()
        self.leading.src = 'images/logo.png'

        self.title = ft.Text()
        self.title.value = 'Flet Tube'
        self.title.color = ft.colors.WHITE

        self.toggle_theme_button = ft.IconButton()
        self.toggle_theme_button.icon = ft.icons.LIGHT_MODE
        self.toggle_theme_button.icon_color = ft.colors.WHITE
        self.actions.append(self.toggle_theme_button)
