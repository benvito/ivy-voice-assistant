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


class ColorTheme(auto):
    DEFAULT = ft.ColorScheme(
        primary="#33363C",
        on_primary="#ffffff",

        primary_container="#2B2E33",
        on_primary_container="#ffffff",

        tertiary="#222428",
        on_tertiary="#ffffff",
        on_tertiary_container="#516279",

        secondary_container="#4D678A",
        on_secondary_container="#ffffff",
   
        secondary="#4D678A",
        on_secondary="#ffffff",

        background="#2B2E33",
        on_background="#393D44",

        outline="#222428",
        outline_variant="#1D1E21",

        scrim="#A7C1E2",
        surface="#222428",
        surface_tint="#82AADF",
        on_surface="#ffffff",
        on_surface_variant="#78A2DB",

        error="#795151",
        on_error="#ffffff",

        surface_variant="#517968"
    )