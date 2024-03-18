import flet as ft
# import time
import asyncio
import threading
from pystray import MenuItem as item
import pystray
from PIL import Image
# import queue
# from pympler import asizeof

from equalizer import Equalizer
from background import Background
from title_bar import AppTitleBar
from buttons import SideBarButton
from side_bar import SideBar   
from main_page import MainPage
from theme import *
from editor_page import EditorPage
from options_page import OptionsPage
from luna_main import Luna
from routing import Routes
# from periodic_task import Periodic
from speech_synthesis.tts import LunaTTS

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
    page.window_visible = True

    page.spacing = 0
    page.padding = 0

    page.fonts = {
        "Jura" : "fonts/Jura.ttf",
    }

    page.theme = ft.Theme(
        font_family="Jura",
        scrollbar_theme=ScrollBarTheme.DEFAULT,
        color_scheme=ColorTheme.DEFAULT
    )

    page.bgcolor="black"

    page_sizes_width = {
        "XXS" : 1100,
        "XS" : 1400,
        "M" : 1600,
        "L" : 1800,
        "XL" : 1900
    }

    luna = Luna()

    # tasks_queue = queue.Queue()

    # async def async_check_variables():
    #     try:
    #         if main_page.equalizer_class.now_audio_play == True and page.route == Routes.MAIN_PAGE and page.window_visible == True:
    #             await main_page.equalizer_class.equalizer_click()

    #         if tasks_queue.qsize() > 0:
    #             task = tasks_queue.get()
    #             await task()
    #     except Exception as e:
    #         print(e)

    async def resize(e):
        page.window_height = page.window_height
        page.window_width = page.window_width
        print("Current window size: ", page.window_width, page.window_height)
        if page.route == Routes.MAIN_PAGE:
            asyncio.create_task(main_page.equalizer_class.active_equalizer())
            main_page.center_items.scale = (page.window_width + page.window_height) / (page.window_max_width + page.window_max_height)
            await main_page.update_async()
            # asyncio.create_task(waiting_for_play())
            
        elif page.route == Routes.OPTIONS_PAGE:
            pass
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
            

    
    async def on_window_event_handler(e):
        pass

    async def on_keyboard_event_handler(e):
        pass

    page.on_window_event = on_window_event_handler
    page.on_keyboard_event = on_keyboard_event_handler

    async def route_change(e : ft.RouteChangeEvent):
        # global check_equalizer
        print("Current route: ", e.route)
        if e.route == Routes.MAIN_PAGE:
            app.controls[cur_page] = main_page
            await app.update_async()
            # asyncio.create_task(main_page.equalizer_class.equlizer_dance.start())
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
    
    
    page.on_route_change = route_change

    page.on_error = lambda e: print(e)
    
    def quit_window(loop : asyncio.ProactorEventLoop):
        page.window_destroy()
        # loop.create_task(wrapper())

    def show_window(loop : asyncio.ProactorEventLoop):
        # print(loop)
        # print(loop.is_running())
        page.window_visible = True
        page.window_to_front()
        page.update()
        # loop.create_task(wrapper())

        # loop.create_task(page.window_to_front_async())
        # loop.create_task(page.update_async())


    async def withdraw_window(e):  
        page.window_visible = False
        await page.update_async()
        await asyncio.sleep(0.05)
    thread_names = [thread.name for thread in list(threading.enumerate())]
    if "tray" not in thread_names:
        main_async_loop = asyncio.get_running_loop()

        image = Image.open("assets/icons/logo256.ico")
        menu = (item('Quit', lambda _: quit_window(loop=main_async_loop)), 
                item('Show', lambda _: show_window(loop=main_async_loop), default=True))
        icon = pystray.Icon("Luna", image, "Luna", menu)
        # icon.run_detached()
        tray_thread = threading.Thread(target=icon.run, name="tray", daemon=True)
        tray_thread.start()

    try:
        icon.update_menu()
    except:
        pass

    # check_equalizer = Periodic(async_check_variables, 0.05)
    # await check_equalizer.start()
    
    # threading.Thread(target=icon.run, name="icon").start()

    title = AppTitleBar(page=page, exit_click=withdraw_window)

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
    
    LunaTTS.equalizer = main_page.equalizer_class
    
    backgroud = Background(ft.RadialGradient(colors=[ft.colors.ON_BACKGROUND, ft.colors.BACKGROUND], radius=0.8))
    cur_page = 1
    page.route = "/"
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

    
    await luna.start_loop()
    
    await page.add_async(
        app
    )

    await page.update_async()

    

ft.app(target=main, assets_dir="assets")
