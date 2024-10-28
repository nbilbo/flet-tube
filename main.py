import traceback
from pathlib import Path
from typing import Callable
from typing import List
from typing import Union

import flet as ft
from pytubefix import YouTube


HOME_DIR = Path.home()


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


class SuccessBanner(ft.Banner):
    def __init__(self) -> None:
        super().__init__()
        self.close_button = ft.TextButton()
        self.close_button.text = 'Close'
        self.close_button.icon = ft.icons.CLOSE
        self.close_button.on_click = self.handle_close
        self.actions.append(self.close_button)

        self.text = ft.Text()
        self.text.theme_style = ft.TextThemeStyle.TITLE_LARGE
        self.text.selectable = True
        self.text.expand = True

        self.icon = ft.Icon()
        self.icon.name = ft.icons.CHECK

        self.content = ft.Row([self.icon, self.text])
        self.bgcolor = ft.colors.GREEN

    def handle_close(self, _event: ft.ControlEvent) -> None:
        self.open = False
        self.update()


class DangerBanner(SuccessBanner):
    def __init__(self) -> None:
        super().__init__()
        self.icon.name = ft.icons.DANGEROUS
        self.bgcolor = ft.colors.RED


class BaseView(ft.View):
    def __init__(self) -> None:
        super().__init__()
        self.appbar = CustomAppBar()

    @ft.View.appbar.getter
    def appbar(self) -> ft.AppBar:
        return super().appbar


class IndexView(BaseView):
    def __init__(self) -> None:
        super().__init__()
        self.route = '/'
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.directory_field = ft.TextField()
        self.directory_field.label = 'Directory'
        self.directory_field.expand = True

        self.directory_picker_button = ft.FloatingActionButton()
        self.directory_picker_button.icon = ft.icons.FOLDER

        self.video_url_field = ft.TextField()
        self.video_url_field.label = 'Youtube Video URL'
        self.video_url_field.expand = True

        self.video_search_button = ft.FloatingActionButton()
        self.video_search_button.icon = ft.icons.SEARCH
        
        search_content = ft.Column()
        search_content.controls.append(ft.Row([self.directory_field, self.directory_picker_button]))
        search_content.controls.append(ft.Row([self.video_url_field, self.video_search_button]))
        self.search_container = ft.Container(search_content)

        self.search_progress_ring = ft.ProgressRing()
        self.search_progress_ring.color = ft.colors.BLUE
        self.search_progress_ring.bgcolor = ft.colors.TRANSPARENT
        self.search_progress_ring.value = 0.0

        self.download_progress_bar = ft.ProgressBar()
        self.download_progress_bar.color = ft.colors.GREEN
        self.download_progress_bar.bgcolor = ft.colors.TRANSPARENT
        self.download_progress_bar.expand = True
        self.download_progress_bar.value = 0.0

        self.video_title = ft.Text()
        self.video_title.size = 20
        self.video_title.selectable = True
        self.video_title.expand = True

        self.video_thumbnail = ft.Image()
        self.video_thumbnail.width = self.video_thumbnail.height = 150
        self.video_thumbnail.fit = ft.ImageFit.SCALE_DOWN
        self.video_thumbnail.src = None

        self.resolution_dropdown = ft.Dropdown()
        self.resolution_dropdown.label = 'Video Resolution'
        self.resolution_dropdown.expand = True

        self.audio_dropdown = ft.Dropdown()
        self.audio_dropdown.label = 'Audio Kbps'
        self.audio_dropdown.expand = True

        self.video_download_button = ft.TextButton()
        self.video_download_button.text = 'Download Video'
        self.video_download_button.icon = ft.icons.DOWNLOAD
        self.video_download_button.icon_color = ft.colors.GREEN

        self.audio_download_button = ft.TextButton()
        self.audio_download_button.text = 'Download Audio'
        self.audio_download_button.icon = ft.icons.DOWNLOAD
        self.audio_download_button.icon_color = ft.colors.GREEN

        video_download_row = ft.Row()
        video_download_row.controls.append(self.resolution_dropdown)
        video_download_row.controls.append(self.video_download_button)

        audio_download_row = ft.Row()
        audio_download_row.controls.append(self.audio_dropdown)
        audio_download_row.controls.append(self.audio_download_button)

        self.download_text = ft.Text()
        self.download_text.theme_style = ft.TextThemeStyle.LABEL_LARGE

        download_content = ft.Column()
        download_content.controls.append(ft.Row([self.video_thumbnail, self.video_title]))
        download_content.controls.append(video_download_row)
        download_content.controls.append(audio_download_row)

        self.download_container = ft.Container(download_content)
        self.download_container.border = ft.border.all(5, ft.colors.TRANSPARENT)
        self.download_container.padding = ft.padding.all(5)

        content = ft.Column()
        content.controls.append(self.search_container)
        content.controls.append(ft.Row([self.search_progress_ring], alignment=ft.MainAxisAlignment.CENTER))
        content.controls.append(ft.Row([self.download_text, self.download_progress_bar]))
        content.controls.append(self.download_container)
        content.scroll = ft.ScrollMode.AUTO
        content.width = 800

        container = ft.Container(content)
        self.controls.append(container)
        container.expand = True


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
        self.set_directory(HOME_DIR)
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


class Handler:
    def __init__(self, application: Application) -> None:
        self.application = application
        self.bind_base_view(self.application.index_view)
        self.bind_index_view(self.application.index_view)

    def bind_base_view(self, view: BaseView) -> None:
        view.appbar.toggle_theme_button.on_click = self.handle_toggle_theme

    def bind_index_view(self, view: IndexView) -> None:
        view.directory_picker_button.on_click = self.handle_open_video_directory_picker
        view.video_search_button.on_click = self.handle_search_video
        view.video_url_field.on_submit = self.handle_search_video
        view.video_download_button.on_click = self.handle_download_video
        view.audio_download_button.on_click = self.handle_download_audio

    def handle_toggle_theme(self, _event: ft.ControlEvent) -> None:
        self.application.toggle_theme()

    def handle_open_video_directory_picker(self, _event: ft.ControlEvent) -> None:
        self.application.open_directory_picker(self.handle_on_result_directory)

    def handle_on_result_directory(self, event: ft.FilePickerResultEvent) -> None:
        self.application.set_directory(event.path)

    def handle_search_video(self, _event: ft.ControlEvent) -> None:
        try:
            self.application.close_banner()
            self.application.hide_download_container()
            self.application.disable_search_container()
            self.application.set_download_progress_value(0.0)
            self.application.set_download_text_value('')
            self.application.start_search_progress_ring()

            youtube = YouTube(self.application.get_video_url())
            streams = youtube.streams.filter(adaptive=True)

            resolutions = {stream.resolution for stream in youtube.streams.filter(adaptive=True,  mime_type='video/mp4')}
            audios = {stream.abr for stream in youtube.streams.filter(adaptive=True, mime_type='audio/mp4')}

            self.application.set_resolutions(list(resolutions))
            self.application.set_audios(list(audios))

        except Exception as error:
            self.application.display_danger_banner(str(error))
            self.application.set_download_progress_value(0.0)
            self.application.set_download_text_value('')
            print(traceback.print_exc())

        else:
            self.application.set_video_thumbnail(youtube.thumbnail_url)
            self.application.set_video_title(youtube.title)
            self.application.show_download_container()

        finally:
            self.application.enable_search_container()
            self.application.stop_search_progress_ring()

    def handle_download_video(self, _event: ft.ControlEvent) -> None:
        try:
            self.application.close_banner()
            self.application.disable_download_container()
            self.application.disable_search_container()
            self.application.set_download_progress_value(None)

            video_url = self.application.get_video_url()
            resolution = self.application.get_resolution()
            video_output = Path(self.application.get_directory()).joinpath('video.mp4')

            youtube_video = YouTube(video_url, on_progress_callback=self.download_video_progress_callback)
            video_stream = youtube_video.streams.filter(adaptive=True, mime_type='video/mp4', res=resolution).first()
            video_stream.download(filename=video_output)

        except Exception as error:
            self.application.display_danger_banner(str(error))
            self.application.set_download_text_value('')
            self.application.set_download_progress_value(0.0)
            print(traceback.print_exc())

        else:
            self.application.set_download_text_value('')
            self.application.set_download_progress_value(0.0)
            self.application.display_success_banner('Video successfully downloaded.')

        finally:
            self.application.set_download_text_value('')
            self.application.set_download_progress_value(0.0)
            self.application.enable_download_container()
            self.application.enable_search_container()

    def handle_download_audio(self, _event: ft.ControlEvent) -> None:
        try:
            self.application.close_banner()
            self.application.disable_download_container()
            self.application.disable_search_container()
            self.application.set_download_progress_value(None)

            video_url = self.application.get_video_url()
            audio = self.application.get_audio()
            audio_output = Path(self.application.get_directory()).joinpath('audio.mp3')
            
            youtube_audio = YouTube(video_url, on_progress_callback=self.download_audio_progress_callback)
            audio_stream = youtube_audio.streams.filter(adaptive=True, mime_type='audio/mp4', abr=audio).first()
            audio_stream.download(filename=audio_output)

        except Exception as error:
            self.application.display_danger_banner(str(error))
            self.application.set_download_text_value('')
            self.application.set_download_progress_value(0.0)
            print(traceback.print_exc())

        else:
            self.application.set_download_text_value('')
            self.application.set_download_progress_value(0.0)
            self.application.display_success_banner('Audio successfully downloaded.')

        finally:
            self.application.set_download_text_value('')
            self.application.set_download_progress_value(0.0)
            self.application.enable_download_container()
            self.application.enable_search_container()

    def download_video_progress_callback(self, stream, _chunk, bytes_remaining) -> None:
        # https://stackoverflow.com/questions/71010685/pytube-us-of-on-progress-callback
        # https://flet.dev/docs/controls/progressbar/
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        self.application.set_download_progress_value(pct_completed * 0.01)
        self.application.set_download_text_value(f'Downloading video {pct_completed:.0f}%')

    def download_audio_progress_callback(self, stream, _chunk, bytes_remaining) -> None:
        # https://stackoverflow.com/questions/71010685/pytube-us-of-on-progress-callback
        # https://flet.dev/docs/controls/progressbar/
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        self.application.set_download_progress_value(pct_completed * 0.01)
        self.application.set_download_text_value(f'Downloading audio {pct_completed:.0f}%')


def main(page: ft.Page) -> None:
    application = Application(page)
    Handler(application)


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
