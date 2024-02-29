import flet as ft
import asyncio

from layouts import FramesRow, PageContainer, CenterContainer, ItemsColumn, ItemsRow
from frames import Frame
from buttons import ClassicButton, ButtonStyle, ContentButton
from theme import *
from utils.utils import IODevices
from utils.yaml_utils import YamlData
from config.config import Config
from config.constants import NAME, INDEX, IO_DEVICES, INPUT_DEVICE, OUTPUT_DEVICE
from main import Luna
import queue


class Option(ft.UserControl):
    def __init__(self,
                control_type : str = "popup",
                popup_items : list = None,
                popup_text : str = None,
                option_name : str = None,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.control_type = control_type
        self.option_name = option_name

        self.popup_button_text = ft.Text(popup_text, size=TextSize.M, color=ft.colors.ON_TERTIARY, expand=10, no_wrap=True)
        if self.control_type == "popup":
            self.option_button = ft.PopupMenuButton(
                                    content=ft.Row(
                                        [
                                            self.popup_button_text,
                                            ft.Image(src="main_images/open_list_button.png", scale=0.8, expand=2)
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    items=popup_items
                                )
        
        self.option_label = ft.Container(
                                    ft.Text(option_name, size=TextSize.M, color=ft.colors.ON_TERTIARY),
                                    margin=ft.margin.only(left=20),
                                    expand=1
                                )

        self.option_container = ft.Container(
                        ItemsRow(
                            [
                                self.option_label,
                                ft.Container(
                                    ft.Container(
                                        self.option_button,
                                        height=100,
                                        margin=ft.margin.symmetric(horizontal=20),
                                    ),
                                    border_radius=15,
                                    width=400,
                                    border=ft.border.all(2, ft.colors.SECONDARY_CONTAINER), 
                                    margin=10,
                                    alignment=ft.alignment.center,  
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        alignment=ft.alignment.center_left,
                        height=70,                       
                    )

        
    def build(self):
        return self.option_container


class CategoryOptions(ft.UserControl):
    def __init__(self,
                 category_label : ft.Text = None,
                 category_options : list = None,
                 divider : ft.Divider = None,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.category_label = category_label
        self.category_options = category_options
        self.divider = divider

        self.category_label_container = ft.Container(
                                content=self.category_label,
                                alignment=ft.alignment.center_left, 
                                margin=ft.margin.symmetric(horizontal=20),
                                bgcolor=ft.colors.TRANSPARENT,
                                border_radius=30,
                                height=50
                            )
        self.category_options_list_with_divider = []
        for i in range(len(self.category_options)):
            self.category_options_list_with_divider.append(
                self.category_options[i]
            )
            if i != len(self.category_options) - 1:
                self.category_options_list_with_divider.append(
                    ft.Container(self.divider, margin=ft.margin.symmetric(horizontal=10), bgcolor=ft.colors.OUTLINE)
                )

        self.category_options_container = ft.Container(
            ItemsColumn(
                self.category_options_list_with_divider,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0
            ),
            alignment=ft.alignment.center,
            margin=0,
            bgcolor=ft.colors.TERTIARY,
            border_radius=30,
        )

        self.category_options_with_label = ItemsColumn(
                                [
                                    self.category_label_container,
                                    self.category_options_container
                                ],
                                spacing=0,
                            )
    # async def update_options_list_with_divider(self):
    #     self.category_options_list_with_divider = []
    #     for i in range(len(self.category_options)):
    #         self.category_options_list_with_divider.append(
    #             self.category_options[i]
    #         )
    #         if i != len(self.category_options) - 1:
    #             self.category_options_list_with_divider.append(
    #                 ft.Container(self.divider, margin=ft.margin.symmetric(horizontal=10), bgcolor=ft.colors.OUTLINE)
    #             )
    #     self.category_options_container.content.controls = self.category_options_list_with_divider
    async def add_option(self, option : Option):
        self.category_options_container.content.controls.append(ft.Container(self.divider, margin=ft.margin.symmetric(horizontal=10), bgcolor=ft.colors.OUTLINE))
        self.category_options_container.content.controls.append(option)
        await self.update_async()

    def build(self):
        return self.category_options_with_label

class OptionsPage(ft.UserControl):
    def __init__(self, 
                 page : ft.Page = None,
                 luna : Luna = None,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.page = page
        self.luna = luna

        self.changed_options_functions = queue.Queue()

        self.save_options_button = ClassicButton(
                            text=ft.Text("СОХРАНИТЬ", color=ft.colors.ON_TERTIARY, size=TextSize.L), 
                            items_alignment=ft.MainAxisAlignment.CENTER,
                            border_radius=ft.border_radius.all(30),
                            tooltip="save options",
                            on_click=self.save_options,
                            bgcolor=ft.colors.ON_TERTIARY_CONTAINER,
                            style=ButtonStyle.SAVE_BUTTON,
                            height=50,
                            width=500,
                            scale=1,
                            disabled=True
                    )
        
        self.input_devices = IODevices.get_input_devices()
        self.output_devices = IODevices.get_output_devices()

        self.config = Config.read_config()

        self.system_setting_input = Option(control_type="popup", 
                           popup_text=self.config[IO_DEVICES][INPUT_DEVICE][NAME], 
                           option_name="УСТРОЙСТВО ВВОДА",
                           popup_items=[
                               ft.TextButton(
                                    content=ft.Container(ft.Text(input_device[NAME], size=TextSize.XS, text_align=ft.TextAlign.START), alignment=ft.alignment.center_left),
                                    style=ButtonStyle.MENU_ITEM_BUTTON,
                                    tooltip=input_device[INDEX],
                                    on_click=self.change_input_device
                                ) for input_device in self.input_devices
                           ]
            )
        
        self.system_setting_output = Option(control_type="popup",
                           popup_text=self.config[IO_DEVICES][OUTPUT_DEVICE][NAME],
                           option_name="УСТРОЙСТВО ВЫВОДА",
                           popup_items=[
                               ft.TextButton(
                                    content=ft.Container(ft.Text(output_devices[NAME], size=TextSize.XS, text_align=ft.TextAlign.START), alignment=ft.alignment.center_left),
                                    style=ButtonStyle.MENU_ITEM_BUTTON,
                                    tooltip=output_devices[INDEX],
                                    on_click=self.change_output_device
                                ) for output_devices in self.output_devices
                           ]
            )

        self.system_setting_options = [
            self.system_setting_input,
            self.system_setting_output,
        ]

        self.system_setting_category = CategoryOptions(
                                category_label=ft.Text("СИСТЕМНЫЕ НАСТРОЙКИ:", size=TextSize.XS, color=ft.colors.ON_TERTIARY),
                                divider=ft.Divider(thickness=2),
                                category_options=self.system_setting_options
                            )

        self.options_column = ItemsColumn(
                        [
                            self.system_setting_category,
                            
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )

        self.options_frame = Frame(
                    content=CenterContainer(
                        self.options_column
                    ),
                    border_radius=30,
                    alignment=ft.alignment.top_center,
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

    async def save_options(self, e : ft.ControlEvent):
        if e.control.tooltip == "save options":
            while not self.changed_options_functions.empty():
                if not self.luna.listen_to_command and not self.luna.process_command:
                    to_update_function = self.changed_options_functions.get()
                    to_update_function() 

            self.save_options_button.disabled_button = True

            self.luna.restart_loop()
            
            await self.save_options_button.update_async()


    async def add_category_options(self, category_option : CategoryOptions):
        self.options_column.controls.append(category_option)
        await self.options_column.update_async()

    async def change_input_device(self, e : ft.ControlEvent):
        name = e.control.content.content.value
        index = e.control.tooltip
        self.config[IO_DEVICES][INPUT_DEVICE][NAME] = name
        self.config[IO_DEVICES][INPUT_DEVICE][INDEX] = index
        Config.write_config(self.config)
        self.system_setting_input.popup_button_text.value = name

        # Save button events
        self.changed_options_functions.put(self.luna.init_recorder)
        self.changed_options_functions.put(self.luna.init_speech_recognizer)
        self.save_options_button.disabled_button = False
        await self.save_options_button.update_async()

        await self.system_setting_input.update_async()

    async def change_output_device(self, e : ft.ControlEvent):
        name = e.control.content.content.value
        index = e.control.tooltip
        self.config[IO_DEVICES][OUTPUT_DEVICE][NAME] = name
        self.config[IO_DEVICES][OUTPUT_DEVICE][INDEX] = index
        Config.write_config(self.config)
        self.system_setting_output.popup_button_text.value = name

        # Save button events
        self.changed_options_functions.put(self.luna.init_tts)
        self.save_options_button.disabled_button = False
        await self.save_options_button.update_async()

        await self.system_setting_output.update_async()


    def build(self):
        return PageContainer(
                self.page_row
            )