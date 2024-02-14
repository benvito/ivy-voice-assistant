import flet as ft


class Background(ft.Container):
    def __init__(self, gradient) -> None:
        super().__init__()

        self.gradient = gradient
        
        self.expand = True
        self.alignment = ft.alignment.center