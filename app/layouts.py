import flet as ft


class FramesRow(ft.Row):
    def __init__(self,
                 controls : list = None,
                 alignment : ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER,
                 vertical_alignment : ft.CrossAxisAlignment = ft.CrossAxisAlignment.CENTER,
                 spacing : int = 26,
                *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.controls = controls
        self.alignment = alignment
        self.vertical_alignment = vertical_alignment
        self.spacing = spacing



class PageContainer(ft.Container):
    def __init__(self,
                content : ft.Control = None,
                 alignment : ft.alignment = ft.alignment.center,
                 expand : bool = True,
                 margin : ft.margin = ft.margin.only(left=131, top=92, bottom=60, right=60),
                *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.content = content
        self.alignment = alignment
        self.expand = expand
        self.margin = margin