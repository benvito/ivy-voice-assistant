import flet as ft
import time
import asyncio
import threading

from equalizer import Equalizer
from background import Background
from title_bar import AppTitleBar
from buttons import SideBarButton, ClassicButton
from side_bar import SideBar   
from main_page import MainPage
from frames import Frame
from layouts import PageContainer, FramesRow, CenterContainer, ItemsColumn
from theme import *
from editor_page import EditorPage
from options_page import OptionsPage
from routing import Routes
from main import Luna


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

    page_sizes_width = {
        "XXS" : 1100,
        "XS" : 1400,
        "M" : 1600,
        "L" : 1800,
        "XL" : 1900
    }

    luna = Luna()


    async def resize(e):
        page.window_height = page.window_height
        page.window_width = page.window_width
        print(page.window_width, page.window_height)
        if page.route == Routes.MAIN_PAGE:
            print("main page")
            main_page.center_items.scale = (page.window_width + page.window_height) / (page.window_max_width + page.window_max_height)
            await main_page.update_async()
        elif page.route == Routes.OPTIONS_PAGE:
            print("options")
        elif page.route == Routes.EDITOR_PAGE:
            editor_page.page_scale = 1 + ((page.window_max_width + page.window_max_height) - (page.window_width + page.window_height)) / 10000
            editor_page.frames_spacing = 26 * ((page.window_width + page.window_height) / (page.window_max_width + page.window_max_height))
            
            if page.window_width < page_sizes_width["XXS"]:
                editor_page.text_size = TextSize.XXS
            elif page.window_width < page_sizes_width["XS"]:
                editor_page.text_size = TextSize.XS
            else:
                editor_page.text_size = TextSize.M

            await editor_page.update_async()
            
            print("editor")
    
    async def on_window_event_handler(e):
        pass

    async def on_keyboard_event_handler(e):
        pass

    page.on_window_event = on_window_event_handler
    page.on_keyboard_event = on_keyboard_event_handler

    async def route_change(e : ft.RouteChangeEvent):
        print(e.route)
        if e.route == Routes.MAIN_PAGE:
            app.controls[cur_page] = main_page
            await app.update_async()
        elif e.route == Routes.OPTIONS_PAGE:
            app.controls[cur_page] = options_page
            await app.update_async()
        elif e.route == Routes.EDITOR_PAGE:
            app.controls[cur_page] = editor_page
            await page.update_async()
        await resize(None)


    async def go_home(e):
        page.route = Routes.MAIN_PAGE
        await page.update_async()

    async def go_options(e):
        page.route = Routes.OPTIONS_PAGE
        await page.update_async()

    async def go_editor(e):
        page.route = Routes.EDITOR_PAGE
        await page.update_async()

    async def restart_luna(e : ft.ControlEvent):
        page.dialog = navigation_rail.dlg_confirm_restart_loop
        navigation_rail.dlg_confirm_restart_loop.open = True
        await page.update_async()  

    page.on_resize = resize
    
    page.fonts = {
        "Jura" : "fonts/Jura.ttf",
    }

    page.theme = ft.Theme(
        font_family="Jura",
        scrollbar_theme=ScrollBarTheme.DEFAULT,
        color_scheme=ColorTheme.DEFAULT
    )

    page.bgcolor="black"
    page.on_route_change = route_change

    title = AppTitleBar(page=page)

    home_button = SideBarButton(img='nav_rail/HOME_nav_rail.png',
                                scale=1,
                                bg_padding=10,
                                button_on_click=go_home)

    options_button = SideBarButton(img='nav_rail/OPTIONS_nav_rail.png',
                                    scale=1,
                                    bg_padding=10,
                                    button_on_click=go_options)

    editor_button = SideBarButton(img='nav_rail/EDITOR_nav_rail.png',
                                scale=1,
                                bg_padding=10,
                                button_on_click=go_editor)
    
    logo = "nav_rail/logo128_nav_rail.png"
 

    restart_button = SideBarButton(img='nav_rail/update_nav_rail.png',
                                   scale=1,
                                   bg_padding=10,
                                   rotate_hover=2,
                                   button_on_click=restart_luna)
    
    navigation_rail = SideBar(buttons=[home_button, editor_button, options_button],
                              restart_button=restart_button,
                              logo=logo,
                              luna=luna)


    main_page = MainPage(luna_img="main_images/luna_center_main_page_clear.png",
                        luna_color=ft.LinearGradient(
                            begin=ft.alignment.center_left,
                            end=ft.alignment.center_right,
                            colors=[
                                ft.colors.SECONDARY_CONTAINER,
                                ft.colors.ON_SURFACE_VARIANT,
                                ft.colors.SURFACE_TINT,
                                ft.colors.SURFACE,
                            ],
                            tile_mode=ft.GradientTileMode.MIRROR),
                        equalizer_class=Equalizer(equalizer_bars_count=12,
                                    equalizer_margin=ft.margin.only(left=20),
                                    equalizer_min_height=20,
                                    equalizer_min_peak_height=40,
                                    equalizer_height=200,
                                    equalizer_spacing_bars=10,
                                    equalizer_speed_dance=0.015,
                                    equalizer_bars_animation=ft.Animation(125, ft.AnimationCurve.FAST_OUT_SLOWIN),
                                    equalizer_color=ft.colors.SCRIM),
                        page=page)
    
    backgroud = Background(ft.RadialGradient(colors=[ft.colors.ON_BACKGROUND, ft.colors.BACKGROUND], radius=0.8))
    cur_page = 1
    page.route = "/options"
    editor_page = EditorPage(page=page, luna=luna)
    options_page = OptionsPage(page=page, luna=luna)
    app = ft.Stack(
            [
                backgroud,
                main_page,
                navigation_rail,
                title,
            ],
            expand=True
        )

    
    luna.start_loop()
    
    await page.add_async(
        app
    )

    await page.update_async()

    

ft.app(target=main, assets_dir="assets")
