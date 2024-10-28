import traceback
from pathlib import Path

import flet as ft
from pytubefix import YouTube

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
