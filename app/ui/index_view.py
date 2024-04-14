import flet as ft

from app.ui import BaseView


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

        self.list_view = ft.ListView()
        self.list_view.spacing = 5
        self.list_view.expand = False

        self.download_text = ft.Text()
        self.download_text.style = ft.TextThemeStyle.LABEL_LARGE

        download_content = ft.Column()
        download_content.controls.append(ft.Row([self.video_thumbnail, self.video_title]))
        download_content.controls.append(self.list_view)

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
        container.expand = True
        self.controls.append(container)
