from typing import Callable, Dict, List, Union

import flet as ft

from app import constants
from app.ui import BaseView, DangerBanner, IndexView, SuccessBanner, VideoPreview


class Application:
    def __init__(self, page: ft.Page) -> None:
        # page settings.
        self.page = page
        self.page.title = 'Flet Tube'
        self.page.on_route_change = self.route_change
        self.page.window_width = self.page.window_height = 550

        # views.
        self.index_view = IndexView()
        self.views: Dict[str, BaseView] = {self.index_view.route: self.index_view}

        # initial state.
        self.go_to_index_view()
        self.index_view.video_url_field.focus()
        self.set_directory(constants.HOME_DIR)
        self.hide_download_container()
        self.display_snack_message('Welcome.')
        self.active_dark_theme()

    def route_change(self, _event: ft.RouteChangeEvent) -> None:
        self.page.views.clear()
        template_route = ft.TemplateRoute(self.page.route)
        if template_route.match(self.index_view.route):
            self.page.views.append(self.index_view)

    def active_dark_theme(self) -> None:
        for view in self.views.values():
            view.appbar.toggle_theme_button.icon = ft.icons.LIGHT_MODE

        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.update()

    def active_light_theme(self) -> None:
        for view in self.views.values():
            view.appbar.toggle_theme_button.icon = ft.icons.DARK_MODE

        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.update()

    def toggle_theme(self) -> None:
        match self.page.theme_mode:
            case ft.ThemeMode.DARK:
                self.active_light_theme()
            case ft.ThemeMode.LIGHT:
                self.active_dark_theme()

    def go_to_index_view(self) -> None:
        self.page.views.append(self.index_view)
        self.page.update()
        #self.page.go(self.index_view.route)

    def open_directory_picker(self, on_result: Callable) -> None:
        picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(picker)
        self.page.update()
        picker.get_directory_path()

    def start_search_progress_ring(self) -> None:
        self.index_view.search_progress_ring.value = None
        self.page.update()

    def stop_search_progress_ring(self) -> None:
        self.index_view.search_progress_ring.value = 0.0
        self.page.update()

    def show_download_container(self) -> None:
        self.index_view.download_container.visible = True
        self.page.update()

    def hide_download_container(self) -> None:
        self.index_view.download_container.visible = False
        self.page.update()

    def disable_download_container(self) -> None:
        self.index_view.download_container.disabled = True
        self.page.update()

    def disable_search_container(self) -> None:
        self.index_view.search_container.disabled = True
        self.page.update()

    def enable_download_container(self) -> None:
        self.index_view.download_container.disabled = False
        self.page.update()

    def enable_search_container(self) -> None:
        self.index_view.search_container.disabled = False
        self.page.update()

    def display_snack_message(self, message: str) -> None:
        snack = ft.SnackBar(ft.Text(message))
        self.page.show_snack_bar(snack)

    def display_success_banner(self, message: str) -> None:
        banner = SuccessBanner()
        banner.text.value = message
        self.page.show_banner(banner)

    def display_danger_banner(self, message: str) -> None:
        banner = DangerBanner()
        banner.text.value = message
        self.page.show_banner(banner)

    def close_banner(self) -> None:
        self.page.close_banner()

    def get_video_url(self) -> str:
        return self.index_view.video_url_field.value

    def get_directory(self) -> str:
        return self.index_view.directory_field.value

    def get_resolution(self) -> str:
        return self.index_view.resolution_dropdown.value

    def get_audio(self) -> str:
        return self.index_view.audio_dropdown.value

    def set_directory(self, directory: str) -> None:
        self.index_view.directory_field.value = directory
        self.page.update()

    def set_video_title(self, title: str) -> None:
        self.index_view.video_title.value = title
        self.page.update()

    def set_video_thumbnail(self, thumbnail: str) -> None:
        self.index_view.video_thumbnail.src = thumbnail
        self.page.update()

    def set_download_progress_value(self, value: Union[float, None]) -> None:
        self.index_view.download_progress_bar.value = value
        self.page.update()

    def set_download_text_value(self, value: str) -> None:
        self.index_view.download_text.value = value
        self.page.update()

    def set_resolutions(self, resolutions: List[str]) -> None:
        self.index_view.resolution_dropdown.options = [ft.dropdown.Option(option) for option in resolutions]
        self.index_view.resolution_dropdown.value = resolutions[0]
        self.page.update()

    def set_audios(self, audios: List[str]) -> None:
        self.index_view.audio_dropdown.options = [ft.dropdown.Option(option) for option in audios]
        self.index_view.audio_dropdown.value = audios[0]
        self.page.update()
