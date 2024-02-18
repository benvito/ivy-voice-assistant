import flet as ft

from layouts import FramesRow, PageContainer, CenterContainer, ItemsColumn, ItemsRow
from frames import Frame
from buttons import ClassicButton, ButtonStyle, ContentButton
from theme import *


class OptionsPage(ft.UserControl):
    def __init__(self, 
                 page : ft.Page = None,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.page = page

        self.save_options_button = ClassicButton(
                            text=ft.Text("СОХРАНИТЬ", color=ft.colors.ON_TERTIARY, size=TextSize.L), 
                            items_alignment=ft.MainAxisAlignment.CENTER,
                            border_radius=ft.border_radius.all(30),
                            tooltip="save options",
                            bgcolor=ft.colors.ON_TERTIARY_CONTAINER,
                            height=50,
                            width=500,
                            scale=1
                    )
        
        self.system_setting_label = ft.Container(
                                content=ft.Text("СИСТЕМНЫЕ НАСТРОЙКИ:", color=ft.colors.ON_TERTIARY, size=TextSize.M),
                                alignment=ft.alignment.center, 
                                bgcolor=ft.colors.ON_TERTIARY_CONTAINER,
                                border_radius=30,
                                height=50
                            )

        self.system_setting_options = ft.Container(
            ItemsColumn(
                [
                    ItemsRow(
                        [
                            ft.Container(
                                ft.Text("УСТРОЙСТВО ВВОДА", size=TextSize.XS, color=ft.colors.ON_TERTIARY),
                                bgcolor=ft.colors.TERTIARY,
                                alignment=ft.alignment.center,
                                border_radius=30,
                                height=40,
                                width=400,


                            ),
                            ft.Container(
                                ft.Text("УСТРОЙСТВО ВЫВОДА", size=TextSize.XS, color=ft.colors.ON_TERTIARY),
                                bgcolor=ft.colors.TERTIARY,
                                alignment=ft.alignment.center,
                                border_radius=30,
                                height=40,
                                width=400,
                            )
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                    ),
                    ItemsRow(
                        [
                            ClassicButton(
                                ft.Text("Какой то микрофон", size=TextSize.M, color=ft.colors.ON_TERTIARY),
                                bgcolor=ft.colors.TERTIARY,
                                alignment=ft.alignment.center,
                                items_alignment=ft.MainAxisAlignment.CENTER,
                                border_radius=60,
                                height=100,
                                expand=1

                            ),
                            ClassicButton(
                                ft.Text("Какой то динамик", size=TextSize.M, color=ft.colors.ON_TERTIARY),
                                bgcolor=ft.colors.TERTIARY,
                                alignment=ft.alignment.center,
                                items_alignment=ft.MainAxisAlignment.CENTER,
                                border_radius=60,
                                height=100,
                                expand=1
                            )
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ]
            ),
            margin=ft.margin.symmetric(horizontal=20),

        )

        self.options_frame = Frame(
                    content=CenterContainer(ItemsColumn(
                        [
                            ItemsColumn(
                                [
                                    self.system_setting_label,
                                    self.system_setting_options
                                ],
                                spacing=20
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )),
                    frame_color=ft.colors.TRANSPARENT,
                    border_color=ft.colors.OUTLINE,
                    border_radius=30,
                    border_width=5,
                    alignment=ft.alignment.center,
                    expand=1
                )
        
        self.page_row = ItemsColumn(
            controls=[
                self.options_frame,
                CenterContainer(
                    self.save_options_button,
                    alignment=ft.alignment.center
                )
            ]
        )

    def build(self):
        return PageContainer(
                self.page_row
            )