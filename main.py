import flet as ft

from app.handler import Handler
from app.ui import Application


def main(page: ft.Page) -> None:
    application = Application(page)
    _handler = Handler(application)


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
