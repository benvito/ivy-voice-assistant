import flet as ft
import sys
import time
import asyncio
import random as rnd

from contextlib import suppress


class Periodic: # https://stackoverflow.com/questions/37512182/how-can-i-periodically-execute-a-function-with-asyncio
    def __init__(self, func, time):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            await asyncio.sleep(self.time)
            await self.func()

### BACKGROUND ###

class Background():
    def __init__(self, page : ft.Page) -> None:
        self.page = page
        self.color1 = "#393D44"
        self.color2 = "#2B2E33"

        self.background = ft.Container(
            # width=page.width,
            # height=page.height,
            gradient=ft.RadialGradient(
                colors=[self.color1, self.color2],
                radius=0.8
            ),
            expand=True,
            alignment=ft.alignment.center
        )

#############

### TITLE ###

class Title():
    def __init__(self, page : ft.Page) -> None:
        self.page = page
        self.title_margin = 6
        self.title_color = "#1D1E21"
        self.title_height = 32
        self.luna_text = "LUNA V1.0"
        self.luna_text_size = 18
        self.title_buttons_scale = 0.6
        self.opacity_elements = 0.5
        self.opacity_hover_button = 0.03

        self.scroll_img = ft.Image(
            src="title/scroll_title_button.png",
            scale=self.title_buttons_scale
        )

        # self.scroll_button = ft.Container(
        #     content=self.scroll_img,
        #     ink=True,
        #     on_click=self.scroll_click
        # )

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


        self.minimize_img = ft.Image(
            src="title/mini_title_button.png",
            scale=self.title_buttons_scale
        )

        # self.minimize_button = ft.Container(
        #     content=self.minimize_img,
        #     ink=True,
        #     on_click=self.minimize_click
        # )

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


        self.exit_img = ft.Image(
            src="title/exit_title_button.png",
            scale=self.title_buttons_scale
        )

        # self.exit_button = ft.Container(
        #     content=self.exit_img,
        #     ink=True,
        #     on_click=self.exit_click
        # )

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

        self.widnow_drag_area = ft.WindowDragArea(
                        self.luna_title_full, 
                        expand=True
                    )


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

        self.title_full = ft.Row([
                    self.widnow_drag_area,
                    self.title_buttons_full
                ],
                spacing=0)

    async def minimize_click(self, e):
        self.page.window_maximized = not self.page.window_maximized
        await self.page.update_async()


    async def scroll_click(self, e):
        self.page.window_minimized = not self.page.window_minimized
        await self.page.update_async()

    
    async def exit_click(self, e):
        await self.page.window_close_async()
        await self.page.update_async()

#############
        
### Navigation Rail ###

class NavigationRail:
    def __init__(self, page):
        self.page = page
        self.rail_color = ft.colors.with_opacity(1, '#222428')
        self.rail_width = 72
        self.rail_margin_top = 35
        self.rail_margin_bottom = 15
        self.scale_button = 2.8
        self.button_bg_padding = 28
        self.button_spacing = 20

        self.scale_hover_button = 0.9
        self.opacity_scale_button = 0.75

        self.rail_button_style = ft.ButtonStyle(
            elevation=0,
            bgcolor=ft.colors.with_opacity(0, '#ffffff'),
            overlay_color=ft.colors.with_opacity(0, "#222428"),
            shape=ft.RoundedRectangleBorder(radius=6),

        )

        self.home_img = ft.Image(
            src="nav_rail/HOME_nav_rail.png"
        )

        self.options_img = ft.Image(
            src="nav_rail/OPTIONS_nav_rail.png"
        )

        self.editor_img = ft.Image(
            src="nav_rail/REDACTOR_nav_rail.png"
        )

        self.home_button_container = ft.Container(
            self.home_img,
            scale=self.scale_button,
            padding=ft.padding.symmetric(vertical=self.button_bg_padding),
            animate_scale=ft.Animation(
                150,
                ft.AnimationCurve.EASE_OUT
            ),
            animate_opacity=ft.Animation(
                150,
                ft.AnimationCurve.LINEAR
            )
        )

        self.options_button_container = ft.Container(
            self.options_img,
            scale=self.scale_button,
            padding=ft.padding.symmetric(vertical=self.button_bg_padding),
            animate_scale=ft.Animation(
                150,
                ft.AnimationCurve.EASE_OUT
            ),
            animate_opacity=ft.Animation(
                150,
                ft.AnimationCurve.LINEAR
            )
        )

        self.editor_button_container = ft.Container(
            self.editor_img,
            scale=self.scale_button,
            padding=ft.padding.symmetric(vertical=self.button_bg_padding),
            animate_scale=ft.Animation(
                150,
                ft.AnimationCurve.EASE_OUT
            ),
            animate_opacity=ft.Animation(
                150,
                ft.AnimationCurve.LINEAR
            )
        )


        self.home_button = ft.ElevatedButton(
            content=self.home_button_container,
            on_click=self.home_click,
            style=self.rail_button_style,
            on_hover=self.on_hover,
        )

        self.options_button = ft.ElevatedButton(
            content=self.options_button_container,
            on_click=self.options_click,
            style=self.rail_button_style,
            on_hover=self.on_hover
        )

        self.editor_button = ft.ElevatedButton(
            content=self.editor_button_container,
            on_click=self.editor_click,
            style=self.rail_button_style,
            on_hover=self.on_hover
        )

        # self.navigation_rail = ft.NavigationRail(
        #     selected_index=0,
        #     label_type=ft.NavigationRailLabelType.ALL,
        #     bgcolor=self.rail_color,
        #     width=self.rail_width,
        #     expand=True,
        #     destinations=[
        #         self.home_img,
                
        #     ]
        # )

        self.rail_column_buttons = ft.Column(
            [
                self.home_button,
                self.editor_button,
                self.options_button
            ],
            spacing=self.button_spacing
        )

        self.rail_logo_img = ft.Image(
                src="nav_rail/logo128_nav_rail.png"
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

        self.navigation_rail = ft.Column(
                expand=True,
                controls=[
                    self.rail_buttons_full,
                    self.rail_logo_full
                ],
                spacing=0
            )

    async def on_hover(self, e : ft.ControlEvent):
        if e.data == 'true':
            e.control.content.animate_scale = ft.Animation(150, ft.AnimationCurve.EASE_OUT)
            e.control.content.scale *= self.scale_hover_button
            e.control.content.opacity *= self.opacity_scale_button
        else:
            e.control.content.animate_scale = ft.Animation(150, ft.AnimationCurve.EASE_IN)
            e.control.content.scale *= round(1 / self.scale_hover_button, 3)
            e.control.content.opacity *= round(1 / self.opacity_scale_button, 3)
        await self.page.update_async()

    def home_click(self, e):
        print("home")
    
    def options_click(self, e):
        print("options")

    def editor_click(self, e):
        print("editor")
            
#############

### EQUALIZER ###
        
class Equalizer(ft.UserControl):
    def __init__(self, 
                 equalizer_bars_count=12,
                 equalizer_margin=ft.margin.only(left=20),
                 equalizer_min_height=20,
                 equalizer_min_peak_height=40,
                 equalizer_height=200,
                 equalizer_spacing_bars=10,
                 equalizer_speed_dance=0.0155,
                 equalizer_bars_animation=ft.Animation(125, ft.AnimationCurve.EASE_IN_OUT),
                 equalizer_color="#A7C1E2") -> None:
        super().__init__()
        self.equalizer_bars_count = equalizer_bars_count
        self.equalizer_margin = equalizer_margin
        self.equalizer_min_height = equalizer_min_height
        self.equalizer_min_peak_height = equalizer_min_peak_height
        self.equalizer_height = equalizer_height
        self.equalizer_spacing_bars = equalizer_spacing_bars
        self.equalizer_speed_dance = equalizer_speed_dance
        self.equalizer_bars_animation = equalizer_bars_animation
        self.equalizer_color = equalizer_color

        self.equlizer_dance = Periodic(self.equalizer_click, 0.05)

        self.equalizer_bars = [ft.Container(width=20, 
                                            height=self.equalizer_min_height, 
                                            bgcolor=self.equalizer_color, 
                                            border_radius=6, 
                                            animate=self.equalizer_bars_animation) 
                                            
                                            for i in range(1, self.equalizer_bars_count + 1)
                                            ]

        self.equalizer_row = ft.Row(
            self.equalizer_bars,
            width=len(self.equalizer_bars) * 20,
            spacing=self.equalizer_spacing_bars,
            height=self.equalizer_height,
        )

    async def equalizer_pick_bar(self, bar):
        bar.height = rnd.randint(self.equalizer_min_peak_height, self.equalizer_row.height)
        await self.update_async()
        await asyncio.sleep(self.equalizer_bars_animation.duration / 1000)
        bar.height = self.equalizer_min_height
        await self.update_async()

    async def equalizer_click(self):
        random_bars = rnd.sample(self.equalizer_bars, len(self.equalizer_bars))
        for bar in random_bars:
            asyncio.create_task(self.equalizer_pick_bar(bar))
            await asyncio.sleep(self.equalizer_speed_dance)

    def build(self):
        return self.equalizer_row
        

### Main page ###

class MainPage():
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.equalizer_class = Equalizer(equalizer_bars_count=12,
                                    equalizer_margin=ft.margin.only(left=20),
                                    equalizer_min_height=20,
                                    equalizer_min_peak_height=60,
                                    equalizer_height=200,
                                    equalizer_spacing_bars=10,
                                    equalizer_speed_dance=0.015,
                                    equalizer_bars_animation=ft.Animation(125, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                    equalizer_color="#A7C1E2")


        self.luna_color = ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[
                    "#587398",
                    "#78A2DB",
                    "#82AADF",
                    "#9FC8FF",
                ],
                tile_mode=ft.GradientTileMode.MIRROR,
        )
        
        self.luna_center_img = ft.Image(
            src="main_images/luna_center_main_page_clear.png"
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

        self.main_page = ft.Container(
            self.center_items_container,
            alignment=ft.alignment.center,
            expand=True
        )

    async def on_hover(self, e):
        if e.data == "true":
            await self.equalizer_class.equlizer_dance.start()
        elif e.data == "false":
            await self.equalizer_class.equlizer_dance.stop()
                
            
                
        
#############

async def main(page: ft.Page):
    page.title = "Luna"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_maximized = True
    page.window_title_bar_buttons_hidden = True
    page.window_title_bar_hidden = True

    page.window_width = 1920
    page.window_height = 1080

    page.window_max_width = 1920
    page.window_max_height = 1080

    page.window_min_width = 854 
    page.window_min_height = 480

    page.window_always_on_top = False

    page.spacing = 0
    page.padding = 0

    async def resize(e):
        await page.update_async()
        page.window_height = page.window_height
        page.window_width = page.window_width
        print(page.window_width, page.window_height)
        main_page.center_items_container.scale = (page.window_width + page.window_height) / (page.window_max_width + page.window_max_height)
        await page.update_async()

    page.on_resize = resize
    
    page.fonts = {
        "Jura" : "fonts/Jura.ttf"
    }

    page.theme = ft.Theme(
        font_family="Jura"
    )

    page.bgcolor="black"

    title = Title(page)
    navigation_rail = NavigationRail(page)
    main_page = MainPage(page)
    app = ft.Stack(
            [
                Background(page).background,
                main_page.main_page,
                navigation_rail.navigation_rail,
                title.title_full,
            ],
            expand=True
        )
    await page.add_async(
        app
    )

    await page.update_async()

ft.app(target=main, assets_dir="assets")