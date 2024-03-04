import flet as ft
import random as rnd
import asyncio
import librosa
import numpy as np
import os
from config import BASE_DIR
from utils.decorators import exec_timer

from periodic_task import Periodic

class Equalizer(ft.UserControl):
    def __init__(self, 
                 equalizer_bars_count=12,
                 equalizer_margin=ft.margin.only(left=20),
                 equalizer_min_height=20,
                 equalizer_min_peak_height=40,
                 equalizer_strength : list = [1,2,3,4,5],
                 equalizer_height=200,
                 equalizer_spacing_bars=10,
                 equalizer_speed_dance=0.0155,
                 equalizer_bars_animation=ft.Animation(125, ft.AnimationCurve.EASE_IN_OUT),
                 equalizer_color=ft.colors.SURFACE,
                 audio_file=os.path.join(BASE_DIR, 'temp', 'luna_answer.mp3')) -> None:
        super().__init__()
        self.equalizer_strength = equalizer_strength

        self._equalizer_data_to_vizualize = None
        self.old_data_to_vizualize = None
        self._audio_file = audio_file
        self._now_audio_play = False
        self._frame_i = 0
        self._chunk_size = 0

        
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

        self.equlizer_dance = Periodic(self.equalizer_click, 0.1)

        self.equalizer_bars = [ft.Container(width=20, 
                                            height=self.equalizer_min_height, 
                                            bgcolor=self.equalizer_color, 
                                            border_radius=6, 
                                            animate=self.equalizer_bars_animation) 
                                            
                                            for i in range(1, self.equalizer_bars_count + 1)
                                            ]
        
        self.range_hz = [[20, 5000], [5001, 10000], [10001, 15000], [15001, 20000]]

        self.equalizer_row = ft.Row(
            self.equalizer_bars,
            width=len(self.equalizer_bars) * 20,
            spacing=self.equalizer_spacing_bars,
            height=self.equalizer_height,
        )

    @property
    def frame_i(self):
        return self._frame_i
    
    @frame_i.setter
    def frame_i(self, value):
        self._frame_i = value

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        self._chunk_size = value

    @property
    def equalizer_data_to_vizualize(self):
        return self._equalizer_data_to_vizualize
    
    @equalizer_data_to_vizualize.setter
    def equalizer_data_to_vizualize(self, value):
        self._equalizer_data_to_vizualize = value

    @property
    def now_audio_play(self):
        return self._now_audio_play

    @now_audio_play.setter
    def now_audio_play(self, value):
        self._now_audio_play = value

    @property
    def audio_file(self):
        return self._audio_file

    @audio_file.setter
    def audio_file(self, value):
        self._audio_file = value
    


    def normalize(self, xi):
        min = np.min(xi)
        max = np.max(xi)
        if min == max:
            return np.zeros_like(xi)
        else:
            return (xi - min) / (max - min)
            

    async def calculate_peak(self, strength) -> tuple:
        # max_peak = self.equalizer_height * strength
        # if max_peak > self.equalizer_height:
        #     max_peak = self.equalizer_height
        # elif max_peak < self.equalizer_min_height:
        #     max_peak = self.equalizer_min_height

        # min_peak = max_peak - self.equalizer_strength_gap
        # if min_peak < self.equalizer_min_peak_height:
        #     min_peak = self.equalizer_min_peak_height

        # if min_peak > max_peak:
        #     min_peak = self.equalizer_height - self.equalizer_strength_gap
        # if max_peak < self.equalizer_min_peak_height:
        #     max_peak = self.equalizer_min_peak_height

        if strength < 0.25:
            strength = 1
        elif strength < 0.4:
            strength = 2
        elif strength < 0.6:
            strength = 3
        elif strength < 0.75:
            strength = 4
        else:
            strength = 5
        min_peak = self.equalizer_min_peak_height + (self.equalizer_strength_gap * strength)
        max_peak = min_peak + self.equalizer_strength_gap
        return int(min_peak), int(max_peak)

    async def equalizer_pick_bar(self, bar, strength):
        min_peak, max_peak = await self.calculate_peak(strength)
        # min_peak = self.equalizer_min_peak_height
        # max_peak = min_peak + self.equalizer_height
        bar.height = rnd.randint(min_peak, max_peak)
        await self.update_async()
        await asyncio.sleep(self.equalizer_bars_animation.duration / 1000)
        bar.height = self.equalizer_min_height
        await self.update_async()

    async def equalizer_click(self):
        if self.now_audio_play and self.equalizer_data_to_vizualize:
            signal = np.frombuffer(self.equalizer_data_to_vizualize, dtype=np.int32)
            normalized_frame = self.normalize(np.abs(signal))
            strength = np.mean(normalized_frame)
            random_bars = rnd.sample(self.equalizer_bars, len(self.equalizer_bars))
            for bar in random_bars:
                asyncio.create_task(self.equalizer_pick_bar(bar, strength))
        # random_bars = rnd.sample(self.equalizer_bars, len(self.equalizer_bars))
        # for bar in random_bars:
        #     asyncio.create_task(self.equalizer_pick_bar(bar, 1))

    def build(self):
        return self.equalizer_row
        