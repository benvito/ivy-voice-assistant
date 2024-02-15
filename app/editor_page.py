import flet as ft
import os
import asyncio
import keyboard
import pyautogui

from layouts import FramesRow, PageContainer, CenterContainer, ItemsColumn
from frames import Frame
from buttons import ClassicButton, ButtonStyle
from theme import *
from utils.yaml_utils import YamlData


class TextEditor(ft.UserControl):
    def __init__(self,
                 bgcolor : str = "#2B2E33",
                 border_radius : ft.border_radius = ft.border_radius.only(bottom_left=20, bottom_right=20),
                 aligment : ft.alignment = ft.alignment.top_center,
                 text_field : ft.TextField = None
                 ) -> None:
        super().__init__()
        self.bgcolor = bgcolor
        self.border_radius = border_radius
        self.aligment = aligment
        
        self.editing_file = None

        self.text_field = text_field
        self.text_field.on_blur = self.on_blur
        self.text_field.on_change = self.on_changed

    async def update_field(self, file_path : str):
        self.editing_file = file_path
        with open(self.editing_file, 'r', encoding="utf-8") as file:
            self.text_field.value = file.read()
            await self.update_async()

    async def on_changed(self, e : ft.ControlEvent):
        print("changed")
    async def on_blur(self, e : ft.ControlEvent):
        if keyboard.is_pressed('tab') or keyboard.is_pressed('tab'):
            await self.text_field.focus_async()
            await asyncio.sleep(0.018)
            pyautogui.write('    ')
        


    def build(self):
        return CenterContainer(
            self.text_field,
            bgcolor=self.bgcolor,
            alignment=self.aligment,
            border_radius=self.border_radius
        )


class EditorPage(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.command_classes = YamlData.load_all_commands_folders()

        self.command_buttons = []
        
        self.editor_window = TextEditor(text_field=ft.TextField(multiline=True, 
                                       border_color=ft.colors.TRANSPARENT, 
                                       value="",
                                       keyboard_type=ft.KeyboardType.MULTILINE))


        for command_class, command_class_path in self.command_classes.items():
            self.command_buttons.append(
                ClassicButton(text=ft.Text(command_class, color=ft.colors.WHITE, size=TextSize.XS), img=ft.Image(src="main_images/command_icon.png"), on_click=self.on_click, tooltip=command_class_path)
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
        
        self.frame_editor = Frame(content=self.editor_window, expand=5)

    async def on_click(self, e : ft.ControlEvent):
        for button in self.command_buttons:
            button.content.bgcolor = '#2B2E33'
            button.content.scale = 1
        e.control.content.bgcolor = '#4D678A'
        e.control.content.scale = 0.95
        await self.editor_window.update_field(os.path.join(e.control.tooltip, "commands.yaml"))
        await self.update_async()


    def build(self):
        return PageContainer(FramesRow([
                    self.frame_commands,
                    self.frame_editor
                    ]))
