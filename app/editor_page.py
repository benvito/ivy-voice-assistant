import flet as ft
import os
import asyncio
import keyboard
import pyautogui

from layouts import FramesRow, PageContainer, CenterContainer, ItemsColumn, ItemsRow
from frames import Frame, SwitchableWindow
from buttons import ClassicButton, ButtonStyle, ContentButton
from theme import *
from utils.yaml_utils import YamlData

class EditorContainer(CenterContainer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            bgcolor=ft.colors.PRIMARY_CONTAINER,
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20),
            margin=ft.margin.only(left=20, right=20, bottom=20)
            ,*args, **kwargs)
       


class TextEditor(ft.UserControl):
    def __init__(self,
                text_field_border_color : str = ft.colors.TRANSPARENT,
                text_field_value : str = '',
                text_field_multiline : bool = True,
                 container : ft.Container = None,
                 ) -> None:
        super().__init__()

        self.editing_file = None

        self.text_field = ft.TextField(
                                    max_lines=None,
                                    multiline=text_field_multiline, 
                                    border_color=text_field_border_color, 
                                    value=text_field_value,
                                    cursor_color=ft.colors.SURFACE,
                                    selection_color=ft.colors.with_opacity(0.3, ft.colors.SURFACE_TINT)
                                    )
        self.text_field.on_blur = self.on_blur
        self.text_field.on_change = self.on_changed

        self.container = container
        self.container.content = self.text_field

    async def update_field(self, file_path : str, update=True):
        self.editing_file = file_path
        with open(self.editing_file, 'r', encoding="utf-8") as file:
            self.text_field.value = file.read()
            if update:
                await self.update_async()

    async def on_changed(self, e : ft.ControlEvent):
        print("changed")
    async def on_blur(self, e : ft.ControlEvent):
        if keyboard.is_pressed('tab') or keyboard.is_pressed('tab'):
            await self.text_field.focus_async()
            await asyncio.sleep(0.018)
            pyautogui.write('    ', interval=0.00)
        

    def build(self):
        return self.container


class DirectoryEditor(ft.UserControl):
    def __init__(self,
                 container : ft.Container = None,):
        super().__init__()
        self.editing_file = None
        self.dirs = []

        self.folder_img = ft.Image(
            src="main_images/folder_editor.png",
            color=ft.colors.PRIMARY,
            color_blend_mode=ft.BlendMode.MODULATE
        )


        self.folder = ft.Container(
            self.folder_img,
            padding=ft.padding.symmetric(vertical=25, horizontal=46),
            bgcolor=ft.colors.TERTIARY
        )

        
        self.container = container
        self.buttons = []
        self.generate_buttons()

        self.buttons_row = ItemsRow(
                self.buttons,
                spacing=30,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                wrap=True,
                run_spacing=30,
                scroll=ft.ScrollMode.AUTO
            )

        self.margin_container = ft.Container(
            self.buttons_row,
            margin=20,
            alignment=ft.alignment.top_center,
        )

        self.container.content = self.margin_container

    async def update_dirs(self, file_path : str, update=True):
        self.editing_file = file_path
        self.dirs = YamlData.load_all_command_subfolders(self.editing_file)
        await self.generate_buttons()
        self.buttons_row.controls = self.buttons
        self.margin_container.content = self.buttons_row
        if update:
            await self.update_async()
    
    async def folder_ico_create(self, text : str):
        return ft.Stack(
                            [
                                self.folder,
                                ft.Container(
                                    ft.Text(
                                        text,
                                        size=TextSize.L,
                                        color=ft.colors.ON_PRIMARY
                                    ), alignment=ft.alignment.center
                                )
                            ],
                            width=240,
                            height=240
                        )

    async def button_ico_create(self, text : str, dir : str):
        return ContentButton(
            content=await self.folder_ico_create(text),
            tooltip=os.path.join(dir, text),
            border_radius=15,
            on_click=self.open_dir_click,
        )

    async def open_dir_click(self, e : ft.ControlEvent):
        os.system(f'start {e.control.tooltip}')

    async def generate_buttons(self):
        self.buttons = []
        for dir in self.dirs:
            folder_ico = await self.button_ico_create(dir, self.editing_file)
            self.buttons.append(folder_ico)


    def build(self):
        return self.container

class EditorWindow(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.text_editor = SwitchableWindow(
            TextEditor(
                container=EditorContainer(alignment=ft.alignment.top_center,)
                )
            )


        self.directories_editor = SwitchableWindow(
                DirectoryEditor(
                    container=EditorContainer(alignment=ft.alignment.top_left,)
                )
            )

        self.current_window = self.text_editor
        self.current_window_name = "edit"
        self.text_editor.is_active = True

    async def update_window(self, window):
        if "dir" in window:
            self.current_window_name = "dir"
            self.current_window = self.directories_editor
            self.text_editor.is_active = False
            self.directories_editor.is_active = True
        if "edit" in window:
            self.current_window_name = "edit"
            self.current_window = self.text_editor
            self.text_editor.is_active = True
            self.directories_editor.is_active = False

        self.controls = [self.current_window]
        await self.update_async()
    def build(self):
        return self.current_window


class EditorPage(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.command_classes = YamlData.load_all_commands_folders()

        self.command_buttons = []
        
        self.editor_window = EditorWindow()


        for command_class, command_class_path in self.command_classes.items():
            self.command_buttons.append(
                ClassicButton(text=ft.Text(command_class, color=ft.colors.WHITE, size=TextSize.XS), img=ft.Image(src="main_images/command_icon.png"), on_click=self.on_command_button_click, tooltip=command_class_path, height=40)
            )

        self.scroll_commands_column =  ItemsColumn(
                                self.command_buttons,
                                scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER,)

        self.frame_commands = Frame(
                        CenterContainer(
                           self.scroll_commands_column,
                            margin=ft.margin.symmetric(vertical=20, horizontal=20),
                            ),
                        expand=2,
                        alignment=ft.alignment.top_left
                        )

        self.edit_button = ft.Container(
                        ClassicButton(
                            text=ft.Text("РЕДАКТОР", color=ft.colors.WHITE, size=TextSize.M), 
                            items_alignment=ft.MainAxisAlignment.CENTER,
                            border_radius=ft.border_radius.only(top_left=30),
                            on_click=self.on_editor_window_button_click,
                            tooltip="edit",
                            height=40,
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            scale=0.98
                            ),
                        expand=1
                    )

        self.directories_button = ft.Container(
                        ClassicButton(
                            text=ft.Text("ПАРАМЕТРЫ", color=ft.colors.WHITE, size=TextSize.M), 
                            items_alignment=ft.MainAxisAlignment.CENTER,
                            border_radius=ft.border_radius.only(top_right=30),
                            on_click=self.on_editor_window_button_click,
                            tooltip="dir",
                            height=40
                            ),
                        expand=1
                    )

        self.editor_buttons_list = [
            self.edit_button,
            self.directories_button
        ]

        self.editor_buttons = CenterContainer(
            content=ItemsRow(
                controls=self.editor_buttons_list,
            ),
            margin=ft.margin.only(top=20, left=20, right=20, bottom=0),
            height=40
        )
        
        self.frame_editor = Frame(content=ItemsColumn(
                                        controls=[
                                            self.editor_buttons, 
                                            ft.Container(self.editor_window, expand=15),
                                          ],
                                          alignment=ft.MainAxisAlignment.START,
                                          horizontal_alignment=ft.CrossAxisAlignment.START,
                                          
                                          ), expand=5)

    async def on_editor_window_button_click(self, e : ft.ControlEvent):
        for button in self.editor_buttons_list:
            button.content.content.bgcolor = ft.colors.PRIMARY_CONTAINER
            button.content.content.scale = 1
        e.control.content.bgcolor = ft.colors.SECONDARY_CONTAINER
        e.control.content.scale = 0.98
        await self.editor_window.update_window(e.control.tooltip)
        await self.update_async()

    async def on_command_button_click(self, e : ft.ControlEvent):
        for button in self.command_buttons:
            button.content.bgcolor = ft.colors.PRIMARY_CONTAINER
            button.content.scale = 1
        e.control.content.bgcolor = ft.colors.SECONDARY_CONTAINER
        e.control.content.scale = 0.98

        await self.editor_window.directories_editor.window.update_dirs(e.control.tooltip, self.editor_window.directories_editor.is_active)
        await self.editor_window.text_editor.window.update_field(os.path.join(e.control.tooltip, "commands.yaml"), self.editor_window.text_editor.is_active)
        await self.update_async()

    def build(self):
        
        return PageContainer(FramesRow([
                    self.frame_commands,
                    self.frame_editor
                    ]))
