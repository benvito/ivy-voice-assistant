import flet as ft
from buttons import SideBarButton        


class SideBar(ft.UserControl):
    def __init__(self,
                 buttons : list,
                 logo : str = None,
                 rail_color : str = ft.colors.with_opacity(1, ft.colors.TERTIARY),
                 rail_width : int = 72,
                 rail_margin_top : int = 35,
                 rail_margin_bottom : int = 15,
                 button_spacing : int = 20):
        super().__init__()

        self.logo = logo

        self.rail_color = rail_color
        self.rail_width = rail_width
        self.rail_margin_top = rail_margin_top
        self.rail_margin_bottom = rail_margin_bottom

        self.buttons = buttons

        self.button_spacing = button_spacing  

        self.rail_column_buttons = ft.Column(
            self.buttons,
            spacing=self.button_spacing
        )

        self.rail_logo_img = ft.Image(
                src=self.logo
            )

        self.rail_logo_container = ft.Container(
                        self.rail_logo_img,
                        alignment=ft.alignment.center,
                        width=self.rail_width,
                        margin=ft.margin.only(bottom=self.rail_margin_bottom)
        )

        self.rail_logo_full = ft.Container(
                        self.rail_logo_container,
                        bgcolor=self.rail_color
        )

        self.rail_buttons_container = ft.Container(
                        self.rail_column_buttons,
                        alignment=ft.alignment.center,
                    )
        
        self.rail_buttons_container_margin = ft.Container(
                        self.rail_buttons_container,
                        margin=ft.margin.symmetric(vertical=self.rail_margin_top),
                        width=self.rail_width,
                    )
        
        self.rail_buttons_full = ft.Container(
                        self.rail_buttons_container_margin,
                        expand=True,
                        bgcolor=self.rail_color
                    )

    def build(self):
        return ft.Column(
                expand=True,
                controls=[
                    self.rail_buttons_full,
                    self.rail_logo_full
                ],
                spacing=0
            )