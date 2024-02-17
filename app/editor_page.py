import flet as ft
import os
import asyncio
import keyboard
import pyautogui
import numpy as np

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
        if file_path:
            with open(self.editing_file, 'r', encoding="utf-8") as file:
                self.text_field.value = file.read()
        else:
            self.text_field.value = ''
        if update:
            await self.update_async()

    async def save_file(self):
        with open(self.editing_file, 'w', encoding="utf-8") as file:
            file.write(self.text_field.value)

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
        for dir in self.dirs:
            folder_ico = ft.Stack(
                            [
                                self.folder,
                                ft.Container(
                                    ft.Text(
                                        dir,
                                        size=TextSize.L,
                                        color=ft.colors.ON_PRIMARY
                                    ), alignment=ft.alignment.center
                                )
                            ],
                            width=240,
                            height=240
                        )
            self.buttons.append(folder_ico)

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
        if file_path:
            self.dirs = YamlData.load_all_command_subfolders(self.editing_file)
            await self.generate_buttons()
            self.buttons_row.controls = self.buttons
            self.margin_container.content = self.buttons_row
        else:
            self.dirs = []
            self.buttons_row.controls = []
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
        self._editing_file = None
        self.text_editor = SwitchableWindow(
            TextEditor(
                container=EditorContainer(alignment=ft.alignment.top_center,)
                )
            )


        self.directories_editor = SwitchableWindow(
                DirectoryEditor(
                    container=EditorContainer(alignment=ft.alignment.top_center,)
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


class CreateCommandDlg(ft.AlertDialog):
    def __init__(self, label : str = "Название команды", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_command_text_field = ft.TextField(
                label=label,
                label_style=ft.TextStyle(color=ft.colors.ON_PRIMARY_CONTAINER),
                border_color=ft.colors.ON_PRIMARY_CONTAINER,
                cursor_color=ft.colors.ON_PRIMARY_CONTAINER
            )
        
        self.content = self.create_command_text_field
        self.modal = True


class ConfirmDlg(ft.AlertDialog):
    def __init__(self,
                cancel_button : ft.TextButton = ft.TextButton(content=ft.Text("Отмена", size=TextSize.XS), style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40),
                confirm_button : ft.TextButton = ft.TextButton(content=ft.Text("Ок", size=TextSize.XS), style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40, autofocus=True),
                confirm_button_on_click : callable = None,
                cancel_button_on_click : callable = None,
                  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modal = True
        confirm_button.on_click = confirm_button_on_click
        if cancel_button_on_click:
            cancel_button.on_click = cancel_button_on_click
        else:
            cancel_button.on_click = self.on_cancel_click
        self.actions = [confirm_button, cancel_button]
    async def on_cancel_click(self, e : ft.ControlEvent):
        self.open = False
        await self.update_async()


class EditorPage(ft.UserControl):
    def __init__(self, page : ft.Page):
        super().__init__()
        self.page = page
        self.page.on_window_event = self.on_window_event_handler
        self.command_classes = YamlData.load_all_commands_folders()

        self.command_buttons = []

        for command_class, command_class_path in self.command_classes.items():
            self.command_buttons.append(
                ClassicButton(text=ft.Text(command_class, color=ft.colors.ON_PRIMARY_CONTAINER, 
                                           size=TextSize.XS), 
                                           img=ft.Image(src="main_images/command_icon.png", color=ft.colors.ON_PRIMARY_CONTAINER), 
                                           on_click=self.on_command_button_click, 
                                           tooltip=command_class_path, 
                                           height=40)
            )
        
        self.editor_window = EditorWindow()
        
        self.no_file_editing_now_snack_bar = ft.SnackBar(
            ft.Text(
                f"Команда не выбрана", 
                color=ft.colors.ON_ERROR, 
                size=TextSize.XS), 
            bgcolor=ft.colors.ERROR
            )

        self.command_saved = ft.SnackBar(
            ft.Text(
                f"Команда сохранена", 
                color=ft.colors.ON_SURFACE, 
                size=TextSize.XS), 
            bgcolor=ft.colors.SURFACE_VARIANT
            )

        self.dlg_create_command = CreateCommandDlg(
            label="Название команды",
            title=ft.Text("СОЗДАТЬ КОМАНДУ", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton(content=ft.Text("Создать", size=TextSize.XS), on_click=self.confirm_create_command, style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40),
                ft.TextButton(content=ft.Text("Отмена", size=TextSize.XS), on_click=self.dlg_create_command_close, style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.dlg_confirm_save = ConfirmDlg(
            title=ft.Text("СОХРАНИТЬ КОМАНДУ?", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            confirm_button_on_click=self.confirm_save_command,
        )

        
        self.add_command_button = ft.Container(
            ClassicButton(img=ft.Image(src="main_images/plus_icon.png", color=ft.colors.ON_PRIMARY_CONTAINER),
                                            bgcolor=ft.colors.ON_TERTIARY_CONTAINER,
                                           on_click=self.on_create_command_click, 
                                           alignment=ft.alignment.center,
                                           items_alignment=ft.MainAxisAlignment.CENTER,
                                           items_vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                           tooltip="create command", 
                                           height=40),
            expand=1
        )

        self.save_command = ft.Container(
            ClassicButton(img=ft.Text("СОХРАНИТЬ", color=ft.colors.ON_PRIMARY_CONTAINER, size=TextSize.M),
                                            bgcolor=ft.colors.ON_TERTIARY_CONTAINER,
                                           on_click=self.save_command_click, 
                                           alignment=ft.alignment.center,
                                           items_alignment=ft.MainAxisAlignment.CENTER,
                                           items_vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                           tooltip="save command", 
                                           height=40),
            expand=1
        )

        self.utils_buttons_row = ItemsRow(
            [self.add_command_button, self.save_command],
        )

        self.scroll_commands_column =  ItemsColumn(
                                self.command_buttons,
                                scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER,)

        self.commands_label =ft.Container(
            ft.Text("КОМАНДЫ:", color=ft.colors.ON_PRIMARY_CONTAINER, size=TextSize.M), 
            alignment=ft.alignment.center, 
            bgcolor=ft.colors.TERTIARY,
            border_radius=30,
            height=40
            )

        self.frame_commands = Frame(content=CenterContainer(
                                    ItemsColumn(
                                        controls=[
                                            self.commands_label, 
                                            ft.Container(self.scroll_commands_column, expand=15),
                                            self.utils_buttons_row
                                          ],
                                          alignment=ft.MainAxisAlignment.START,
                                          horizontal_alignment=ft.CrossAxisAlignment.START,
                                          
                                          ),
                                    margin=ft.margin.symmetric(vertical=20, horizontal=20),
                                    ),
                                    expand=2)

        self.edit_button = ft.Container(
                        ClassicButton(
                            text=ft.Text("РЕДАКТОР", color=ft.colors.ON_PRIMARY_CONTAINER, size=TextSize.M), 
                            items_alignment=ft.MainAxisAlignment.CENTER,
                            border_radius=ft.border_radius.only(top_left=30),
                            on_click=self.on_editor_window_button_click,
                            tooltip="edit",
                            height=40,
                            scale=0.98
                            ),
                        expand=1
                    )
        
        self.edit_button.content.content.bgcolor = ft.colors.SECONDARY_CONTAINER

        self.directories_button = ft.Container(
                        ClassicButton(
                            text=ft.Text("ПАРАМЕТРЫ", color=ft.colors.ON_PRIMARY_CONTAINER, size=TextSize.M), 
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
        
    async def on_window_event_handler(self, e : ft.ControlEvent):
        await self.update_commands_buttons()
        button_selected = await self.current_command_button_selected()
        if button_selected is None:
            await self.update_editor(button_selected)
        else:
            await self.update_editor_dir(button_selected)
        await self.update_async()
        
    async def update_commands_buttons(self):
        new_command_classes = YamlData.load_all_commands_folders()

        if new_command_classes != self.command_classes:
            old_buttons = self.command_buttons
            intersection = set(new_command_classes.values()) & set(self.command_classes.values())
            
            self.command_classes = new_command_classes

            self.command_buttons = []

            for command_class, command_class_path in self.command_classes.items():
                if command_class_path not in intersection:
                    command_button = ClassicButton(text=ft.Text(command_class, color=ft.colors.ON_PRIMARY_CONTAINER, 
                                                size=TextSize.XS), 
                                                img=ft.Image(src="main_images/command_icon.png", color=ft.colors.ON_PRIMARY_CONTAINER), 
                                                on_click=self.on_command_button_click, 
                                                tooltip=command_class_path, 
                                                height=40)
                else:
                    for button in old_buttons:
                        if button.tooltip == command_class_path:
                            command_button = button
                self.command_buttons.append(
                    command_button
                )

            self.scroll_commands_column.controls = self.command_buttons
    async def confirm_save_command(self, e : ft.ControlEvent):
        if self.editor_window.current_window.window.editing_file is not None:
            await self.editor_window.text_editor.window.save_file()
            self.page.snack_bar = self.command_saved
            self.page.snack_bar.open = True
        else:
            self.page.snack_bar = self.no_file_editing_now_snack_bar
            self.page.snack_bar.open = True
        
        
        self.dlg_confirm_save.open = False
        
        await self.page.update_async()

    async def save_command_click(self, e : ft.ControlEvent):
        self.page.dialog = self.dlg_confirm_save
        self.dlg_confirm_save.open = True
        await self.page.update_async()

    async def confirm_create_command(self, e : ft.ControlEvent):
        YamlData.create_command_folder(self.dlg_create_command.create_command_text_field.value)
        
        await self.update_commands_buttons()
        await self.dlg_create_command_close(e)
        
        await self.update_async()

    async def dlg_create_command_close(self, e : ft.ControlEvent):
        self.dlg_create_command.open = False
        
        await self.page.update_async()

    async def on_create_command_click(self, e : ft.ControlEvent):
        self.dlg_create_command.create_command_text_field.value = ""
        
        self.page.dialog = self.dlg_create_command
        self.dlg_create_command.open = True
        
        await self.page.update_async()

    async def current_command_button_selected(self):
        for button in self.command_buttons:
            if button.is_secected:
                return button

    async def on_editor_window_button_click(self, e : ft.ControlEvent):
        if e.control.is_secected == False:
            for button in self.editor_buttons_list:
                button.content.content.bgcolor = ft.colors.PRIMARY_CONTAINER
                button.content.content.scale = 1
                button.content.is_secected = False
            
            await self.button_select(e)
            await self.editor_window.update_window(e.control.tooltip)
            await self.update_async()

    async def button_select(self, e : ft.ControlEvent):
        e.control.content.bgcolor = ft.colors.SECONDARY_CONTAINER
        e.control.content.scale = 0.98
        e.control.is_secected = True

    async def update_editor(self, button):
        if button:
            await self.editor_window.directories_editor.window.update_dirs(button.tooltip, self.editor_window.directories_editor.is_active)
            await self.editor_window.text_editor.window.update_field(os.path.join(button.tooltip, "commands.yaml"), self.editor_window.text_editor.is_active)
        else:
            await self.editor_window.directories_editor.window.update_dirs(None, self.editor_window.directories_editor.is_active)
            await self.editor_window.text_editor.window.update_field(None, self.editor_window.text_editor.is_active)
    
    async def update_editor_dir(self, button):
        if button:
            await self.editor_window.directories_editor.window.update_dirs(button.tooltip, self.editor_window.directories_editor.is_active)
        else:
            await self.editor_window.directories_editor.window.update_dirs(None, self.editor_window.directories_editor.is_active)
    
    async def update_editor_text(self, button):
        if button:
            await self.editor_window.text_editor.window.update_field(os.path.join(button.tooltip, "commands.yaml"), self.editor_window.text_editor.is_active)
        else:
            await self.editor_window.text_editor.window.update_field(None, self.editor_window.text_editor.is_active)
    
    async def on_command_button_click(self, e : ft.ControlEvent):
        if e.control.is_secected == False:
            for button in self.command_buttons:
                button.content.bgcolor = ft.colors.PRIMARY_CONTAINER
                button.content.scale = 1
                button.is_secected = False
            
            await self.button_select(e)
            await self.update_editor(e.control)
            await self.update_async()

    def build(self):
        
        return PageContainer(FramesRow([
                    self.frame_commands,
                    self.frame_editor
                    ]))
