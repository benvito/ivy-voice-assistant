import flet as ft
from enum import auto

class ScrollBarTheme(auto):
    DEFAULT = ft.ScrollbarTheme(
        thumb_color={
            ft.MaterialState.DEFAULT: ft.colors.with_opacity(0.15, '#000000'),
        },
        track_border_color = ft.colors.TRANSPARENT,
        thickness=15,
        radius=10,
        cross_axis_margin=0,
        main_axis_margin=5,
        min_thumb_length=50
    )


class TextSize(auto):
    XXS = 12
    XS = 18
    M = 24
    L = 36
    XL = 48
    XXL = 60
    XXXL = 72