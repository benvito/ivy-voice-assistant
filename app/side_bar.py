import flet as ft
from buttons import SideBarButton, ButtonStyle   
from theme import *
from main import Luna
from enum import auto


class SideBarSnackBars(auto):
    RESTART_LOOP_SUCCESS = ft.SnackBar(
            ft.Text(
                f"Ядро успешно перезагружено", 
                color=ft.colors.ON_SURFACE, 
                size=TextSize.XS), 
            bgcolor=ft.colors.SURFACE_VARIANT,
            duration=1500
            )

class SideBar(ft.UserControl):
    def __init__(self,
                 luna : Luna,
                 buttons : list,
                 logo : str = None,
                 rail_color : str = ft.colors.with_opacity(1, ft.colors.TERTIARY),
                 rail_width : int = 72,
                 rail_margin_top : int = 35,
                 rail_margin_bottom : int = 15,
                 button_spacing : int = 20,
                 restart_button = None):
        super().__init__()

        self.luna = luna

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

        # self.rail_logo_img = ft.Image(
        #         src=self.logo
        #     )

        # self.rail_logo_container = ft.Container(
        #                 self.rail_logo_img,
        #                 alignment=ft.alignment.center,
        #                 width=self.rail_width,
        #                 margin=ft.margin.only(bottom=self.rail_margin_bottom)
        # )

        # self.rail_logo_full = ft.Container(
        #                 self.rail_logo_container,
        #                 bgcolor=self.rail_color
        # )

        self.dlg_confirm_restart_loop = ft.AlertDialog(
            title=ft.Text("ПЕРЕЗАГРУЗИТЬ ЯДРО ЛУНЫ?", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.CENTER,
            actions=[
                ft.TextButton(content=ft.Text("Ок", size=TextSize.XS), style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40, autofocus=True, on_click=self.confirm_restart_loop),
                ft.TextButton(content=ft.Text("Отмена", size=TextSize.XS), style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40, on_click=self.close_dlg)
            ]
        )

        self.rail_restart_button = restart_button

        self.rail_restart_button_container = ft.Container(
                    self.rail_restart_button,
                    alignment=ft.alignment.center,
                    width=self.rail_width,
                    margin=ft.margin.only(bottom=self.rail_margin_bottom),
        )

        self.rail_restart_button_full = ft.Container(
                    self.rail_restart_button_container,
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
    
    async def confirm_restart_loop(self, e):
        await self.luna.restart_loop()
        self.dlg_confirm_restart_loop.open = False
        self.page.snack_bar = SideBarSnackBars.RESTART_LOOP_SUCCESS
        self.page.snack_bar.open = True
        await self.page.update_async()

    async def close_dlg(self, e):
        self.dlg_confirm_restart_loop.open = False
        await self.page.update_async()

    def build(self):
        return ft.Column(
                expand=True,
                controls=[
                    self.rail_buttons_full,
                    self.rail_restart_button_full
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )