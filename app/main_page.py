import flet as ft
from equalizer import Equalizer

class MainPage(ft.UserControl):
    def __init__(self, luna_img : str, luna_color : ft.LinearGradient, equalizer_class : Equalizer) -> None:  
        super().__init__()
        self.luna_img = luna_img
        self.luna_color = luna_color

        self.equalizer_class = equalizer_class

        self.luna_center_img = ft.Image(
            src=self.luna_img
        )

        self.luna_center_shader = ft.ShaderMask(
            self.luna_center_img,
            shader=self.luna_color
        )

        self.luna_center_container = ft.Container(
            self.luna_center_shader,
            scale=1,
            padding=0,
            on_hover=self.on_hover
        )

        self.equalizer_container = ft.Container(
            self.equalizer_class,
            alignment=ft.alignment.center,
            width=self.equalizer_class.equalizer_row.width,
            margin=self.equalizer_class.equalizer_margin,
        )

        self.center_items = ft.Stack(
                [
                    ft.Row([self.equalizer_container], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.luna_center_container], alignment=ft.MainAxisAlignment.CENTER),
                ],
                expand=False,
                height=500
            )

        self.center_items_container = ft.Container(
            self.center_items,
            padding=0,
        )

    async def on_hover(self, e):
        if e.data == "true":
            await self.equalizer_class.equlizer_dance.start()
        elif e.data == "false":
            await self.equalizer_class.equlizer_dance.stop()

    def build(self):
        return ft.Container(
            self.center_items_container,
            alignment=ft.alignment.center,
            expand=True
        )    
        