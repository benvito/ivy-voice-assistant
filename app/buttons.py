import flet as ft
from enum import auto
from layouts import FramesRow
from theme import ColorTheme

class ButtonStyle(auto):
    NO_BORDER_BG = ft.ButtonStyle(
            elevation=0,
            bgcolor=ft.colors.with_opacity(0, ft.colors.ON_TERTIARY),
            overlay_color=ft.colors.with_opacity(0, ft.colors.TERTIARY),
            shape=ft.RoundedRectangleBorder(radius=6),
            padding=0
        )

    SELECTED_BUTTON = ft.ButtonStyle(
        bgcolor=ft.colors.SECONDARY,
        overlay_color=ft.colors.with_opacity(0, ft.colors.TERTIARY),
        shape=ft.RoundedRectangleBorder(radius=6),
        padding=2
    )


class ContentButton(ft.ElevatedButton):
    def __init__(self,
                 content : ft.Control = None,
                 border_radius : ft.border_radius = ft.border_radius.all(30),
                 bgcolor : str = None,
                 animation_scale : ft.Animation = ft.Animation(100, ft.AnimationCurve.EASE_IN_OUT),
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = ft.Container(
            content,
            bgcolor=bgcolor,
            border_radius=border_radius,
            animate_scale=animation_scale
        )

        self.style = ButtonStyle.NO_BORDER_BG


class ClassicButton(ft.ElevatedButton):
    def __init__(self,
                 text : ft.Text = None,
                 img : ft.Image = None,
                 content : ft.Control = None,
                 scale : float = 1,
                 height : int = None,
                 bgcolor : str = ft.colors.PRIMARY_CONTAINER,
                 margin : int = None,
                 alignment : ft.alignment = ft.alignment.center_left,
                 border_radius : ft.border_radius = ft.border_radius.all(30),
                 items_alignment : ft.MainAxisAlignment = ft.MainAxisAlignment.START,
                 items_vertical_alignment : ft.CrossAxisAlignment = ft.CrossAxisAlignment.CENTER,
                 animation_scale : ft.Animation = ft.Animation(100, ft.AnimationCurve.EASE_IN_OUT),
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button_items = [img, text, content]
        self.button_items = [x for x in self.button_items if x is not None]
        self.button_container = ft.Container(
            ft.Container(
                FramesRow(
                    self.button_items,
                    alignment=items_alignment,
                    vertical_alignment=items_vertical_alignment,
                    spacing=10
                ),
                margin=ft.margin.only(left=20 if len(self.button_items) > 1 else 0),
            ),
            height=height,
            bgcolor=bgcolor,
            alignment=alignment,
            border_radius=border_radius,
            margin=margin,
            animate_scale=animation_scale,
            scale=scale
        )
        self.content = self.button_container
        self.style = ButtonStyle.NO_BORDER_BG
        

class SideBarButton(ft.ElevatedButton):
    def __init__(self, 
                 img : str,
                 scale : float = 1, 
                 bg_padding : float = None,
                 button_on_click : callable = None,
                 scale_hover : float = 0.9,
                 opacity_scale : float = 0.75,
                 color : str = ft.colors.ON_TERTIARY_CONTAINER,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_button = color
        self.scale_hover_button = scale_hover
        self.opacity_scale_button = opacity_scale
        self.button_on_click = button_on_click
        self.button_bg_padding = bg_padding
        self.img = img
        self.scale_button = scale
        self.rail_button_style = ButtonStyle.NO_BORDER_BG

        self.button_img = ft.Image(
            src=self.img,
            color=self.color_button
        )

        self.button_container = ft.Container(
            self.button_img,
            scale=self.scale_button,
            padding=ft.padding.symmetric(vertical=self.button_bg_padding),
            animate_scale=ft.Animation(
                150,
                ft.AnimationCurve.EASE_OUT
            ),
            animate_opacity=ft.Animation(
                150,
                ft.AnimationCurve.LINEAR
            )
        )

        self.content = self.button_container
        self.style = self.rail_button_style

        self.on_click = self.button_on_click
        self.on_hover = self.button_on_hover
    
    async def button_on_hover(self, e : ft.ControlEvent):
        if e.data == 'true':
            e.control.content.animate_scale = ft.Animation(150, ft.AnimationCurve.EASE_OUT)
            e.control.content.scale *= self.scale_hover_button
            e.control.content.opacity *= self.opacity_scale_button
        else:
            e.control.content.animate_scale = ft.Animation(150, ft.AnimationCurve.EASE_IN)
            e.control.content.scale *= round(1 / self.scale_hover_button, 3)
            e.control.content.opacity *= round(1 / self.opacity_scale_button, 3)
        await e.control.update_async()