import flet as ft


class SuccessBanner(ft.Banner):
    def __init__(self) -> None:
        super().__init__()
        self.close_button = ft.TextButton()
        self.close_button.text = 'Close'
        self.close_button.icon = ft.icons.CLOSE
        self.close_button.on_click = self.handle_close
        self.actions.append(self.close_button)

        self.text = ft.Text()
        self.text.style = ft.TextThemeStyle.TITLE_LARGE
        self.text.selectable = True
        self.text.expand = True

        self.icon = ft.Icon()
        self.icon.name = ft.icons.CHECK

        self.content = ft.Row([self.icon, self.text])
        self.bgcolor = ft.colors.GREEN

    def handle_close(self, _event: ft.ControlEvent) -> None:
        self.open = False
        self.update()
