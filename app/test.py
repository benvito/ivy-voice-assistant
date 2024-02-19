# -*- coding: utf-8 -*-

import pyaudio
p = pyaudio.PyAudio()

devices = p.get_device_count()

for i in range(devices):
   device_info = p.get_device_info_by_index(i)
   if device_info.get('maxInputChannels') > 0 and device_info.get('hostApi') == 2:
        print(f"Микрофон: {device_info.get('name').encode('cp1251').decode('utf-8')} , Device Index: {device_info.get('index')}")