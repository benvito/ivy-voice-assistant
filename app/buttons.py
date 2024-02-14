import flet as ft


class ClassicButton(ft.ElevatedButton):
    def __init__(self):
        pass

class SideBarButton(ft.ElevatedButton):
    def __init__(self, 
                 img : str,
                 scale : float = 1, 
                 bg_padding : float = None,
                 button_on_click : callable = None,
                 scale_hover : float = 0.9,
                 opacity_scale : float = 0.75,
                 color : str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_button = color
        self.scale_hover_button = scale_hover
        self.opacity_scale_button = opacity_scale
        self.button_on_click = button_on_click
        self.button_bg_padding = bg_padding
        self.img = img
        self.scale_button = scale
        self.rail_button_style = ft.ButtonStyle(
            elevation=0,
            bgcolor=ft.colors.with_opacity(0, '#ffffff'),
            overlay_color=ft.colors.with_opacity(0, "#222428"),
            shape=ft.RoundedRectangleBorder(radius=6),
        )

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