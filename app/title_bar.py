import flet as ft
from theme import *

class AppTitleBar(ft.Row):
    def __init__(self, page : ft.Page, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.page = page
        self.title_margin = 6
        self.title_color = "#1D1E21"
        self.title_height = 32
        self.luna_text = "LUNA V1.0"
        self.luna_text_size = TextSize.XS
        self.title_buttons_scale = 0.6
        self.opacity_elements = 0.5
        self.opacity_hover_button = 0.03
        
        ### SCROLL BUTTON ###
        self.scroll_img = ft.Image(
            src="title/scroll_title_button.png",
            scale=self.title_buttons_scale
        )

        self.scroll_button = ft.TextButton(
            text="━",
            on_click=self.scroll_click,
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.HOVERED: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                    ft.MaterialState.FOCUSED: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                    ft.MaterialState.DEFAULT: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                },
                overlay_color=ft.colors.with_opacity(self.opacity_hover_button, '#ffffff')
            ),
            width=40
        )

        ### MINIMIZE BUTTON ###
        self.minimize_img = ft.Image(
            src="title/mini_title_button.png",
            scale=self.title_buttons_scale
        )

        self.minimize_button = ft.IconButton(
            icon=ft.icons.CROP_SQUARE_ROUNDED,
            on_click=self.minimize_click,
            icon_size=20,
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.HOVERED: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                    ft.MaterialState.FOCUSED: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                    ft.MaterialState.DEFAULT: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                },
                overlay_color=ft.colors.with_opacity(self.opacity_hover_button, '#ffffff')
            )
        )

        ### EXIT BUTTON ###
        self.exit_img = ft.Image(
            src="title/exit_title_button.png",
            scale=self.title_buttons_scale
        )

        self.exit_button = ft.IconButton(
            icon=ft.icons.CLOSE_ROUNDED,
            on_click=self.exit_click,
            icon_size=20,
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.HOVERED: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                    ft.MaterialState.FOCUSED: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                    ft.MaterialState.DEFAULT: ft.colors.with_opacity(self.opacity_elements, '#ffffff'),
                },
                overlay_color=ft.colors.with_opacity(self.opacity_hover_button, '#ffffff')
            )
        )

        ### LUNA TITLE ###
        self.luna_version_text = ft.Container(
            ft.Text(self.luna_text, color=ft.colors.with_opacity(self.opacity_elements, '#ffffff'), size=self.luna_text_size),
            alignment=ft.alignment.center_left
        )

        self.luna_margin_title = ft.Container(
                                self.luna_version_text,
                                margin=ft.margin.symmetric(horizontal=self.title_margin),
                            )

        self.luna_title_full = ft.Container(
                            self.luna_margin_title,
                            height=self.title_height,
                            bgcolor=self.title_color
                        )

        ### WINDOW DRAG AREA ###
        self.widnow_drag_area = ft.WindowDragArea(
                        self.luna_title_full, 
                        expand=True
                    )

        ### TITLE BUTTONS ###
        self.title_buttons = ft.Container(
                                    ft.Row([self.scroll_button, self.minimize_button, self.exit_button]),
                                )

        self.title_buttons_margin = ft.Container(
                            self.title_buttons,
                            margin=ft.margin.symmetric(horizontal=self.title_margin),
                        )

        self.title_buttons_full = ft.Container(
                        self.title_buttons_margin,
                        height=self.title_height,
                        bgcolor=self.title_color
                    )
        
        # flet.Row() PARAMETERS #
        self.spacing = 0
        self.controls = [self.widnow_drag_area, self.title_buttons_full]

    async def minimize_click(self, e):
        self.page.window_maximized = not self.page.window_maximized
        await self.page.update_async()


    async def scroll_click(self, e):
        self.page.window_minimized = not self.page.window_minimized
        await self.page.update_async()

    
    async def exit_click(self, e):
        await self.page.window_close_async()
        await self.page.update_async()