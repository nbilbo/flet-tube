import traceback
from pathlib import Path

import flet as ft
from moviepy.editor import VideoFileClip
from pytube import YouTube

from app.ui import Application, BaseView, IndexView, VideoPreview


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

    def bind_videos_previews(self) -> None:
        for preview in self.application.get_videos_previews():
            preview.download_button.on_click = (lambda _event, video_preview=preview: self.handle_download_video(video_preview))

    def handle_toggle_theme(self, _event: ft.ControlEvent) -> None:
        self.application.toggle_theme()

    def handle_open_video_directory_picker(self, _event: ft.ControlEvent) -> None:
        self.application.open_directory_picker(self.handle_on_result_video_directory)

    def handle_on_result_video_directory(self, event: ft.FilePickerResultEvent) -> None:
        self.application.set_video_directory(event.path)

    def handle_search_video(self, _event: ft.ControlEvent) -> None:
        try:
            self.application.close_banner()
            self.application.hide_download_container()
            self.application.disable_search_container()
            self.application.set_download_progress_value(0.0)
            self.application.set_download_text_value('')
            self.application.start_search_progress_ring()

            youtube = YouTube(self.application.get_video_url())
            streams = youtube.streams.filter(progressive=True)[::-1]

        except Exception as error:
            self.application.display_danger_banner(str(error))
            self.application.set_download_progress_value(0.0)
            self.application.set_download_text_value('')
            print(traceback.print_exc())

        else:
            self.application.set_streams(streams)
            self.application.set_video_thumbnail(youtube.thumbnail_url)
            self.application.set_video_title(youtube.title)
            self.application.show_download_container()
            self.bind_videos_previews()

        finally:
            self.application.enable_search_container()
            self.application.stop_search_progress_ring()

    def handle_download_video(self, video_preview: VideoPreview) -> None:
        try:
            stream = video_preview.stream
            filename = stream.title.replace(' ', '-') + '.mp4'
            output_path = self.application.get_video_directory()

            self.application.close_banner()
            self.application.disable_download_container()
            self.application.disable_search_container()
            self.application.set_download_progress_value(None)
            self.application.set_download_text_value('Downloading...')
            stream.download(output_path=output_path, filename=filename)

            if video_preview.converter_checkbox.value:
                file = Path.joinpath(Path(output_path), Path(filename))
                self.application.set_download_text_value('Converting...')
                self.convert_to_mp3(str(file))

            self.application.display_success_banner('Done.')

        except Exception as error:
            self.application.display_danger_banner(str(error))
            self.application.set_download_text_value('')
            self.application.set_download_progress_value(0.0)
            print(traceback.print_exc())

        finally:
            self.application.set_download_text_value('')
            self.application.set_download_progress_value(0.0)
            self.application.enable_download_container()
            self.application.enable_search_container()

    def download_progress_callback(self, stream, _chunk, bytes_remaining) -> None:
        # https://stackoverflow.com/questions/71010685/pytube-us-of-on-progress-callback
        # https://flet.dev/docs/controls/progressbar/
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        self.application.set_download_progress_value(pct_completed * 0.01)
        self.application.set_download_text_value(f'Downloading {pct_completed:.0f}%')

    def convert_to_mp3(self, file: str) -> None:
        # https://github.com/NeuralNine/youtube-downloader-converter/blob/master/file_converter.py
        clip = VideoFileClip(file)
        clip.audio.write_audiofile(file[:-4] + '.mp3')
        clip.close()
