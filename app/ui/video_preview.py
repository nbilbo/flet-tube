from typing import Optional

import flet as ft
from pytube import Stream


class VideoPreview(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.stream: Optional[Stream] = None

        self.resolution = ft.Text()
        self.resolution.style = ft.TextThemeStyle.LABEL_LARGE

        self.download_button = ft.TextButton()
        self.download_button.icon = ft.icons.DOWNLOAD
        self.download_button.text = 'Download'
        self.download_button.icon_color = ft.colors.GREEN

        self.converter_checkbox = ft.Checkbox()
        self.converter_checkbox.label = 'Convert to MP3'

        content = ft.Column()
        content.controls.append(
            ft.Row([self.resolution, self.download_button, self.converter_checkbox])
        )

        self.container = ft.Container(content)
        self.container.border = ft.border.all(3, '#A66F5B')
        self.container.padding = ft.padding.all(15)

    def build(self) -> ft.Container:
        return self.container
