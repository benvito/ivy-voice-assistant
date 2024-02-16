import flet as ft

class SwitchableWindow(ft.UserControl):
    def __init__(self, window, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.is_active = False
        self.window = window
    
    def build(self):
        return self.window

class Frame(ft.Container):
    def __init__(self,
                 content : ft.Control = None,
                 frame_color : str = '#33363C',
                 border_color : str = '#222428',
                 border_radius : int = 50,
                 border_width : int = 9,
                 width : int = None,
                 height : int = None,
                 expand : int = False,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.content = content
        self.bgcolor = frame_color
        self.border = ft.border.all(border_width, border_color)
        self.border_radius = border_radius
        self.width = width
        self.height = height
        self.expand = expand

        