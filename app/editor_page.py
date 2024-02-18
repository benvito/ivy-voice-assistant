import flet as ft
import os
import asyncio
import keyboard
import pyautogui
import numpy as np
import enum

from layouts import FramesRow, PageContainer, CenterContainer, ItemsColumn, ItemsRow
from frames import Frame, SwitchableWindow
from buttons import ClassicButton, ButtonStyle, ContentButton
from theme import *
from utils.yaml_utils import YamlData

class EmptyContentText(enum.auto):
    NONE = ft.Text('', color=ft.colors.ON_PRIMARY)
    VARIANT1 = ft.Text('Тут пока пусто, но ты можешь это поменять...', 
                       color=ft.colors.with_opacity(0.25, ft.colors.ON_PRIMARY),
                       size=TextSize.M
                       )

class EditorContainer(CenterContainer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            bgcolor=ft.colors.PRIMARY_CONTAINER,
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20),
            margin=0,
            *args, **kwargs)
       

class TextEditor(ft.UserControl):
    def __init__(self,
                 bgcolor : str = ft.colors.TRANSPARENT,
                text_field_border_color : str = ft.colors.TRANSPARENT,
                container_field_border_color : str = ft.colors.OUTLINE,
                text_field_value : str = '',
                text_field_multiline : bool = True,
                 container : ft.Container = None,
                 ) -> None:
        super().__init__()

        self.editing_file = None

        self.base_text_field_value = text_field_value

        self.text_field = ft.TextField(
                                    max_lines=None,
                                    multiline=text_field_multiline, 
                                    border_color=text_field_border_color,
                                    border_width=5,
                                    color=ft.colors.ON_PRIMARY,
                                    hint_text=EmptyContentText.VARIANT1.value,
                                    hint_style=ft.TextStyle(color=ft.colors.with_opacity(0.25, ft.colors.ON_PRIMARY)),
                                    value=self.base_text_field_value,
                                    cursor_color=ft.colors.SURFACE,
                                    selection_color=ft.colors.with_opacity(0.3, ft.colors.SURFACE_TINT)
                                    )

        self.text_field.on_change = self.on_changed

        self.container = container
        self.container.on_click = self.on_click_container
        self.container.content = self.text_field
        self.container.border = ft.border.all(2, ft.colors.with_opacity(1, container_field_border_color))

    async def update_field(self, file_path : str, update=True):
        self.editing_file = file_path
        if file_path:
            with open(self.editing_file, 'r', encoding="utf-8") as file:
                self.text_field.value = file.read()
        else:
            self.text_field.value = self.base_text_field_value
        if update:
            await self.update_async()

    async def on_click_container(self, e : ft.ControlEvent):
        await self.text_field.focus_async()

    async def save_file(self):
        with open(self.editing_file, 'w', encoding="utf-8") as file:
            file.write(self.text_field.value)


    async def on_changed(self, e : ft.ControlEvent):
        pass
    async def tab_pressed(self):
        await self.text_field.focus_async()
        await asyncio.sleep(0.018)
        pyautogui.write("    ", interval=0.00)
        

    def build(self):
        return self.container


class DirectoryEditor(ft.UserControl):
    def __init__(self,
                 container : ft.Container = None,
                 empty_content_text : ft.Text = EmptyContentText.VARIANT1):
        super().__init__()
        self.editing_file = None
        self.empty_content_text = empty_content_text
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
            if len(self.buttons) > 0:
                self.buttons_row.controls = self.buttons
            else:
                self.buttons_row.controls = [
                    self.empty_content_text
                    ]
        else:
            self.dirs = []
            self.buttons_row.controls = []
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
        os.startfile(f'{e.control.tooltip}')

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
                    container=EditorContainer(alignment=ft.alignment.top_center,)
                )
            )

        self.current_window = self.text_editor
        self.current_window_name = "edit"
        self.text_editor.is_active = True 
    
    @property
    def text_editor_field_value(self):
        return self.text_editor.window.text_field.value

    @text_editor_field_value.setter
    def text_editor_field_value(self, value):
        self.text_editor.window.text_field.value = value

    @property
    def editing_file(self):
        return self.text_editor.window.editing_file

    @editing_file.setter
    def editing_file(self, value):
        self.text_editor.window.editing_file = value

    @property
    def editing_dir(self):
        return self.directories_editor.window.editing_file

    @editing_dir.setter
    def editing_dir(self, value):
        self.directories_editor.window.editing_file = value

    # @property
    # def text_editor(self):
    #     return self.text_editor.window
    
    # @text_editor.setter
    # def text_editor(self, value):
    #     self.text_editor.window = value

    # @property
    # def directories_editor(self):
    #     return self.directories_editor.window

    # @directories_editor.setter
    # def directories_editor(self, value):
    #     self.directories_editor.window = value

    # @property
    # def directories_editor_is_active(self):
    #     return self.directories_editor.is_active
    
    # @directories_editor_is_active.setter
    # def directories_editor_is_active(self, value):
    #     self.directories_editor.is_active = value

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


# class Dialogs(enum.auto):
#     CREATE_COMMAND = CreateCommandDlg(
#             label="Название команды",
#             title=ft.Text("СОЗДАТЬ КОМАНДУ", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
#             actions=[
#                 ft.TextButton(content=ft.Text("Создать", size=TextSize.XS), on_click=self.confirm_create_command, style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40),
#                 ft.TextButton(content=ft.Text("Отмена", size=TextSize.XS), on_click=self.dlg_create_command_close, style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40),
#             ],
#             actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
#         )

#     DELETE_COMMAND = ConfirmDlg(
#             title=ft.Text("УДАЛИТЬ КОМАНДУ?", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
#             actions_alignment=ft.MainAxisAlignment.CENTER,
#             confirm_button_on_click=self.confirm_delete_command,
#         )

#     SAVE_COMMAND = ConfirmDlg(
#             title=ft.Text("СОХРАНИТЬ КОМАНДУ?", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
#             actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#             confirm_button_on_click=self.confirm_save_command,
#         )

class EditorSnackBars(enum.auto):
    NO_FILE_EDITING_NOW = ft.SnackBar(
            ft.Text(
                f"Команда не выбрана", 
                color=ft.colors.ON_ERROR, 
                size=TextSize.XS), 
            bgcolor=ft.colors.ERROR
            )

    COMMAND_SAVED = ft.SnackBar(
            ft.Text(
                f"Команда сохранена", 
                color=ft.colors.ON_SURFACE, 
                size=TextSize.XS), 
            bgcolor=ft.colors.SURFACE_VARIANT
            )
    
    COMMAND_DELETED = ft.SnackBar(
            ft.Text(
                f"Команда удалена",
                color=ft.colors.ON_SURFACE,
                size=TextSize.XS
            ),
            bgcolor=ft.colors.SURFACE_VARIANT
    )

    ERROR_SAVING = ft.SnackBar(
            ft.Text(
                f"Не удалось сохранить", 
                color=ft.colors.ON_ERROR, 
                size=TextSize.XS), 
            bgcolor=ft.colors.ERROR
            )



class EditorPage(ft.UserControl):
    def __init__(self, page : ft.Page):
        super().__init__()
        self.page = page

        self.deleting_command = None

        self.command_classes = YamlData.load_all_commands_folders()

        self.command_buttons = []

        for command_class, command_class_path in self.command_classes.items():
            self.command_buttons.append(
                ClassicButton(text=ft.Text(command_class, color=ft.colors.ON_PRIMARY_CONTAINER, 
                                           size=TextSize.XS), 
                                           img=ft.Image(src="main_images/command_icon.png", color=ft.colors.ON_PRIMARY_CONTAINER),
                                           on_click=self.on_command_button_click, 
                                           extra_content=ClassicButton(img=ft.Image(src="main_images/exit_icon.png", scale=0.75),
                                                    bgcolor=ft.colors.TRANSPARENT,
                                                    items_alignment=ft.MainAxisAlignment.CENTER,
                                                    alignment=ft.alignment.center,
                                                    items_vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    on_click=self.on_delete_command_cilck,
                                                    tooltip=f"delete:{command_class}",
                                                    height=40),
                                           tooltip=command_class_path, 
                                           height=40,)                
            )
        
        self.editor_window = EditorWindow()

        self.dlg_create_command = ft.AlertDialog(
            content=ft.TextField(
                label="Название команды",
                label_style=ft.TextStyle(color=ft.colors.ON_PRIMARY_CONTAINER),
                border_color=ft.colors.ON_PRIMARY_CONTAINER,
                cursor_color=ft.colors.ON_PRIMARY_CONTAINER
            ),
            title=ft.Text("СОЗДАТЬ КОМАНДУ", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton(content=ft.Text("Создать", size=TextSize.XS), on_click=self.confirm_create_command, style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40),
                ft.TextButton(content=ft.Text("Отмена", size=TextSize.XS), on_click=self.close_dlg, style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.dlg_confirm_save = ft.AlertDialog(
            title=ft.Text("СОХРАНИТЬ КОМАНДУ?", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            actions=[
                ft.TextButton(content=ft.Text("Ок", size=TextSize.XS), style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40, autofocus=True, on_click=self.confirm_save_command),
                ft.TextButton(content=ft.Text("Отмена", size=TextSize.XS), style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40, on_click=self.close_dlg)
            ]
        )

        self.dlg_confirm_delete_command = ft.AlertDialog(
            title=ft.Text("УДАЛИТЬ КОМАНДУ?", color=ft.colors.ON_PRIMARY_CONTAINER, text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.CENTER,
            actions=[
                ft.TextButton(content=ft.Text("Ок", size=TextSize.XS), style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40, autofocus=True, on_click=self.confirm_delete_command),
                ft.TextButton(content=ft.Text("Отмена", size=TextSize.XS), style=ButtonStyle.TEXT_BUTTON_ON_PRIMARY, width=150, height=40, on_click=self.close_dlg)
            ]
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

        self.editor_buttons = ft.Container(
            content=ItemsRow(
                controls=self.editor_buttons_list,
            ),
            # margin=ft.margin.only(top=20, left=20, right=20, bottom=0),
            height=40
        )

        self.open_command_dir_button = ClassicButton(
                        text=ft.Text(
                            "ОТКРЫТЬ ПАПКУ",
                            size=TextSize.M,
                            color=ft.colors.ON_PRIMARY_CONTAINER
                        ),
                        bgcolor=ft.colors.ON_TERTIARY_CONTAINER,
                        height=40,
                        items_alignment=ft.MainAxisAlignment.CENTER,
                        on_click=self.on_open_command_dir_click
                    )
        
        self.frame_editor = Frame(content=CenterContainer(
                                    content=ItemsColumn(
                                            controls=[
                                                self.editor_buttons, 
                                                ft.Container(self.editor_window, expand=15),
                                                self.open_command_dir_button
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                    margin=ft.margin.symmetric(vertical=20, horizontal=20),
                                    ), 
                                expand=5)

    async def on_open_command_dir_click(self, e : ft.ControlEvent):
        if self.editor_window.editing_dir is not None:
            os.startfile(f'{self.editor_window.editing_dir}')
        else:
            self.page.snack_bar = EditorSnackBars.NO_FILE_EDITING_NOW
            self.page.snack_bar.open = True
            await self.page.update_async()    
    
    
    async def close_dlg(self, e : ft.ControlEvent):
        self.page.dialog.open = False
        await self.page.update_async()

    async def on_keyboard_event_handler(self, e : ft.KeyboardEvent):
        if e.key == "Tab" and "edit" in self.editor_window.current_window_name:
            await self.editor_window.text_editor.window.tab_pressed()
    
    async def confirm_delete_command(self, e : ft.ControlEvent):
        YamlData.delete_command_folder(self.deleting_command)
        await self.update_commands_buttons()
        self.dlg_confirm_delete_command.open = False
        await self.update_editor_page_content()
        await self.page.update_async()


    async def on_delete_command_cilck(self, e : ft.ControlEvent):
        self.deleting_command = e.control.tooltip.split(':')[-1]
        self.page.dialog = self.dlg_confirm_delete_command
        self.dlg_confirm_delete_command.open = True
        await self.page.update_async()

    async def update_editor_page_content(self):
        await self.update_commands_buttons()
        if self.page:
            button_selected = await self.current_command_button_selected()
            if button_selected is None:
                await self.update_editor(button_selected)
            else:
                await self.update_editor_dir(button_selected)
            
            await self.update_async()
        
    async def on_window_event_handler(self, e : ft.ControlEvent):
        await self.update_editor_page_content()
        
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
                                           extra_content=ClassicButton(img=ft.Image(src="main_images/exit_icon.png", scale=0.75),
                                                    bgcolor=ft.colors.TRANSPARENT,
                                                    items_alignment=ft.MainAxisAlignment.CENTER,
                                                    alignment=ft.alignment.center,
                                                    items_vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                    on_click=self.on_delete_command_cilck,
                                                    tooltip=f"delete:{command_class}",
                                                    height=40),
                                           tooltip=command_class_path, 
                                           height=40,)  
                else:
                    for button in old_buttons:
                        if button.tooltip == command_class_path:
                            command_button = button
                self.command_buttons.append(
                    command_button
                )

            self.scroll_commands_column.controls = self.command_buttons

    async def confirm_save_command(self, e : ft.ControlEvent):
        if self.editor_window.editing_file is not None:
            try:
                await self.editor_window.text_editor.window.save_file()
                self.page.snack_bar = EditorSnackBars.COMMAND_SAVED
                self.page.snack_bar.open = True
            except Exception as e:
                self.page.snack_bar = EditorSnackBars.ERROR_SAVING
                self.page.snack_bar.open = True
        else:
            self.page.snack_bar = EditorSnackBars.NO_FILE_EDITING_NOW
            self.page.snack_bar.open = True
        
        
        self.dlg_confirm_save.open = False
        
        await self.page.update_async()

    async def save_command_click(self, e : ft.ControlEvent):
        self.page.dialog = self.dlg_confirm_save
        self.dlg_confirm_save.open = True
        await self.page.update_async()

    async def confirm_create_command(self, e : ft.ControlEvent):
        YamlData.create_command_folder(self.dlg_create_command.content.value)
        
        await self.update_commands_buttons()
        await self.dlg_create_command_close(e)
        
        await self.update_async()

    async def dlg_create_command_close(self, e : ft.ControlEvent):
        self.dlg_create_command.open = False
        
        await self.page.update_async()

    async def on_create_command_click(self, e : ft.ControlEvent):
        self.dlg_create_command.content.value = ""
        
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
                button.content.background_color = ft.colors.PRIMARY_CONTAINER
                button.content.scaling = 1
                button.content.is_secected = False
            
            await self.button_select(e)
            await self.editor_window.update_window(e.control.tooltip)
            await self.update_async()

    async def button_select(self, e : ft.ControlEvent):
        e.control.background_color = ft.colors.SECONDARY_CONTAINER
        e.control.scaling = 0.98
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
                button.background_color = ft.colors.PRIMARY_CONTAINER
                button.scaling = 1
                button.is_secected = False
            
            await self.button_select(e)
            await self.update_editor(e.control)
            await self.update_async()

    def build(self):
        return PageContainer(FramesRow([
                    self.frame_commands,
                    self.frame_editor
                    ]))
