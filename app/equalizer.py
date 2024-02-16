import flet as ft
import random as rnd
import asyncio

from periodic_task import Periodic

class Equalizer(ft.UserControl):
    def __init__(self, 
                 equalizer_bars_count=12,
                 equalizer_margin=ft.margin.only(left=20),
                 equalizer_min_height=20,
                 equalizer_min_peak_height=40,
                 equalizer_strength : list = [1,2,3],
                 equalizer_height=200,
                 equalizer_spacing_bars=10,
                 equalizer_speed_dance=0.0155,
                 equalizer_bars_animation=ft.Animation(125, ft.AnimationCurve.EASE_IN_OUT),
                 equalizer_color=ft.colors.SURFACE) -> None:
        super().__init__()
        self.equalizer_strength = equalizer_strength
        
        self.equalizer_bars_count = equalizer_bars_count
        self.equalizer_margin = equalizer_margin
        self.equalizer_min_height = equalizer_min_height
        self.equalizer_min_peak_height = equalizer_min_peak_height
        self.equalizer_height = equalizer_height
        self.equalizer_spacing_bars = equalizer_spacing_bars
        self.equalizer_speed_dance = equalizer_speed_dance
        self.equalizer_bars_animation = equalizer_bars_animation
        self.equalizer_color = equalizer_color

        self.equalizer_strength_gap = (self.equalizer_height - self.equalizer_min_peak_height) / (len(self.equalizer_strength) + 1)

        self.equlizer_dance = Periodic(self.equalizer_click, 0.05)

        self.equalizer_bars = [ft.Container(width=20, 
                                            height=self.equalizer_min_height, 
                                            bgcolor=self.equalizer_color, 
                                            border_radius=6, 
                                            animate=self.equalizer_bars_animation) 
                                            
                                            for i in range(1, self.equalizer_bars_count + 1)
                                            ]

        self.equalizer_row = ft.Row(
            self.equalizer_bars,
            width=len(self.equalizer_bars) * 20,
            spacing=self.equalizer_spacing_bars,
            height=self.equalizer_height,
        )

    async def calculate_peak(self, strength) -> tuple:
        min_peak = self.equalizer_min_peak_height + (self.equalizer_strength_gap * strength)
        max_peak = min_peak + self.equalizer_strength_gap
        return int(min_peak), int(max_peak)

    async def equalizer_pick_bar(self, bar, strength):
        min_peak, max_peak = await self.calculate_peak(strength)
        bar.height = rnd.randint(min_peak, max_peak)
        await self.update_async()
        await asyncio.sleep(self.equalizer_bars_animation.duration / 1000)
        bar.height = self.equalizer_min_height
        await self.update_async()

    async def equalizer_click(self):
        strength = rnd.choice(self.equalizer_strength)
        random_bars = rnd.sample(self.equalizer_bars, len(self.equalizer_bars))
        for bar in random_bars:
            asyncio.create_task(self.equalizer_pick_bar(bar, strength))
            await asyncio.sleep(self.equalizer_speed_dance)

    def build(self):
        return self.equalizer_row
        