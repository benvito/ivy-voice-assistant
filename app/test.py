# import wave
# import pyaudio
# from utils.utils import IODevices

# def play_mono_audio(file_path, output_device_index):
#     wf = wave.open(file_path, 'rb')

#     p = pyaudio.PyAudio()

#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True,
#                     output_device_index=output_device_index)

#     data = wf.readframes(1024)

#     while data:
#         stream.write(data)
#         data = wf.readframes(1024)

#     stream.stop_stream()
#     stream.close()

#     p.terminate()

# if __name__ == "__main__":
#    p = pyaudio.PyAudio()
#    devices = p.get_device_count()
#    for i in range(devices):
#       device_info = p.get_device_info_by_index(i)
#       if device_info.get('maxInputChannels') > 0:
#           print(f"{device_info.get('name').encode('cp1251').decode('utf-8')} - i:{device_info.get('index')} - api:{device_info.get('hostApi')}")
#    audio_file_path = "output.mp3"

#    output_device_index = 5
#    play_mono_audio(audio_file_path, output_device_index)

#    #  for device_index in range(pyaudio.PyAudio().get_device_count()):
#    #    try:
#    #       output_device_index = device_index

#    #       play_mono_audio(audio_file_path, output_device_index)
#    #    except:
#    #       print(F"Error {device_index}")


# import numpy as np

# ar1 = [[1], [2], [3]]
# ar2 = [[4], [5], [6]]
# ar3 = [[7], [8], [9]]

# arr = np.concatenate((ar1, ar2, ar3), axis=0)

# arr = np.reshape(arr, (4, 1))
# print(arr)

# from attrdict import AttrDict
# from config.config import Config

# config_dict = Config.read_config()
# config = AttrDict(**config_dict)
# print(config.models.wake_word)

# class Luna:
#     def __init__(self):
#         self.text = "test"
#     def print(self):
#         print(self.text)


# from config import BASE_DIR
# import os

# # Загрузите аудиофайл
# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
# import numpy as np

# # Загрузка аудиофайла
# audio_file = os.path.join(BASE_DIR, 'temp', 'gg.wav')

# y, sr = librosa.load(audio_file)

# # Определение размера фрейма (в отсчетах)
# frame_size = 1024

# # Вычисление громкости для каждого фрейма
# amplitudes = []
# for i in range(0, len(y), frame_size):
#     frame = y[i:i+frame_size]
#     amplitude = np.sqrt(np.mean(frame**2))  # RMS amplitude
#     amplitudes.append(amplitude)

# # Создание временной оси
# time = np.arange(0, len(y)/sr, frame_size/sr)

# # Построение графика громкости для каждого фрейма
# plt.figure(figsize=(12, 4))
# librosa.display.waveshow(y, sr=sr, alpha=0.5, label='Waveform')
# plt.plot(time, amplitudes, color='r', label='Amplitude (RMS) for each frame')
# plt.title('График громкости для каждого фрейма аудиофайла')
# plt.xlabel('Время (сек)')
# plt.ylabel('Амплитуда')
# plt.legend()
# plt.show()


# from config import BASE_DIR
# import os
# import wave
# import numpy as np
# import matplotlib.pyplot as plt

# # Загрузка аудиофайла
# audio_file = os.path.join(BASE_DIR, 'temp', 'luna_answer.mp3')
# wf = wave.open(audio_file, 'rb')

# # Получение параметров аудиофайла
# channels = wf.getnchannels()
# sample_width = wf.getsampwidth()
# frame_rate = wf.getframerate()
# num_frames = wf.getnframes()

# # Чтение данных из аудиофайла
# raw_data = wf.readframes(num_frames)
# wf.close()

# # Преобразование байтовых данных в массив NumPy
# signal = np.frombuffer(raw_data, dtype=np.int16)

#     # Если у аудиофайла два канала, усредним их
# if channels == 2:
#     signal = (signal[::2] + signal[1::2]) / 2

# signal = np.array(signal, dtype=np.float32)

# # Нормализация амплитуды от 0 до 1
# normalized_signal = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
# print(normalized_signal)

# data = np.array([-0.5, 0, 0.2, 0.8, -0.3, 1])

# # Нормализация данных от 0 до 1
# normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))

# print("Исходные данные:", data)
# print("Нормализованные данные:", normalized_data)
# # Построение графика
# time = np.linspace(0, num_frames / frame_rate, num_frames)
# plt.figure(figsize=(12, 4))
# plt.plot(time, normalized_signal, color='b', label='Нормализованный сигнал')
# plt.title('График нормализованной громкости аудиофайла')
# plt.xlabel('Время (сек)')
# plt.ylabel('Нормализованная амплитуда')
# plt.legend()
# plt.show()

# from config import BASE_DIR
# import os
# import pyaudio
# import numpy as np
# from pydub import AudioSegment

# def play_audio_frames(audio_file, frame_size=1024, overlap=1):
#     # Загрузка аудиофайла
#     audio = AudioSegment.from_file(audio_file)

#     # Получение параметров аудио
#     channels = audio.channels
#     frame_rate = audio.frame_rate
#     frame_count = len(audio)

#     # Преобразование аудио в массив NumPy
#     samples = np.array(audio.get_array_of_samples())

#     # Разделение аудио на фреймы
#     for i in range(0, frame_count - frame_size, overlap):
#         frame = samples[i:i + frame_size]

#         # Воспроизведение фрейма с использованием pyaudio
#         p = pyaudio.PyAudio()
#         stream = p.open(format=pyaudio.paInt16,
#                         channels=channels,
#                         rate=frame_rate,
#                         output=True)

#         stream.write(frame.tobytes())
#         stream.close()
#         p.terminate()

# # Замените "path_to_your_audio_file.wav" на путь к вашему аудиофайлу
# audio_file = os.path.join(BASE_DIR, 'temp', 'gg.wav')
# play_audio_frames(audio_file)


#!/usr/bin/env python
# Module     : SysTrayIcon.py
# Synopsis   : Windows System tray icon.
# Programmer : Simon Brunning - simon@brunningonline.net - modified for Python 3
# Date       : 13 February 2018
# Notes      : Based on (i.e. ripped off from) Mark Hammond's
#              win32gui_taskbar.py and win32gui_menu.py demos from PyWin32
# '''TODO

# For now, the demo at the bottom shows how to use it...'''

# from config import BASE_DIR
# import os
# import sys
# import win32api         # package pywin32
# import win32con
# import win32gui_struct
# try:
#     import winxpgui as win32gui
# except ImportError:
#     import win32gui

# class SysTrayIcon(object):
#     '''TODO'''
#     QUIT = 'QUIT'
#     SPECIAL_ACTIONS = [QUIT]

#     FIRST_ID = 1023

#     def __init__(self,
#                  icon,
#                  hover_text,
#                  menu_options,
#                  on_quit=None,
#                  default_menu_index=None,
#                  window_class_name=None,):

#         self.icon = icon
#         self.hover_text = hover_text
#         self.on_quit = on_quit

#         menu_options = menu_options + (('Quit', None, self.QUIT),)
#         self._next_action_id = self.FIRST_ID
#         self.menu_actions_by_id = set()
#         self.menu_options = self._add_ids_to_menu_options(list(menu_options))
#         self.menu_actions_by_id = dict(self.menu_actions_by_id)
#         del self._next_action_id


#         self.default_menu_index = (default_menu_index or 0)
#         self.window_class_name = window_class_name or "SysTrayIconPy"

#         message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
#                        win32con.WM_DESTROY: self.destroy,
#                        win32con.WM_COMMAND: self.command,
#                        win32con.WM_USER+20 : self.notify,}
#         # Register the Window class.
#         window_class = win32gui.WNDCLASS()
#         hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
#         window_class.lpszClassName = self.window_class_name
#         window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
#         window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
#         window_class.hbrBackground = win32con.COLOR_WINDOW
#         window_class.lpfnWndProc = message_map # could also specify a wndproc.
#         classAtom = win32gui.RegisterClass(window_class)
#         # Create the Window.
#         style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
#         self.hwnd = win32gui.CreateWindow(classAtom,
#                                           self.window_class_name,
#                                           style,
#                                           0,
#                                           0,
#                                           win32con.CW_USEDEFAULT,
#                                           win32con.CW_USEDEFAULT,
#                                           0,
#                                           0,
#                                           hinst,
#                                           None)
#         win32gui.UpdateWindow(self.hwnd)
#         self.notify_id = None
#         self.refresh_icon()

#         win32gui.PumpMessages()

#     def _add_ids_to_menu_options(self, menu_options):
#         result = []
#         for menu_option in menu_options:
#             option_text, option_icon, option_action = menu_option
#             if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
#                 self.menu_actions_by_id.add((self._next_action_id, option_action))
#                 result.append(menu_option + (self._next_action_id,))
#             elif non_string_iterable(option_action):
#                 result.append((option_text,
#                                option_icon,
#                                self._add_ids_to_menu_options(option_action),
#                                self._next_action_id))
#             else:
#                 print('Unknown item', option_text, option_icon, option_action)
#             self._next_action_id += 1
#         return result

#     def refresh_icon(self):
#         # Try and find a custom icon
#         hinst = win32gui.GetModuleHandle(None)
#         if os.path.isfile(self.icon):
#             icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
#             hicon = win32gui.LoadImage(hinst,
#                                        self.icon,
#                                        win32con.IMAGE_ICON,
#                                        0,
#                                        0,
#                                        icon_flags)
#         else:
#             print("Can't find icon file - using default.")
#             hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

#         if self.notify_id: message = win32gui.NIM_MODIFY
#         else: message = win32gui.NIM_ADD
#         self.notify_id = (self.hwnd,
#                           0,
#                           win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
#                           win32con.WM_USER+20,
#                           hicon,
#                           self.hover_text)
#         win32gui.Shell_NotifyIcon(message, self.notify_id)

#     def restart(self, hwnd, msg, wparam, lparam):
#         self.refresh_icon()

#     def destroy(self, hwnd, msg, wparam, lparam):
#         if self.on_quit: self.on_quit(self)
#         nid = (self.hwnd, 0)
#         win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
#         win32gui.PostQuitMessage(0) # Terminate the app.
#         return 0

#     def notify(self, hwnd, msg, wparam, lparam):
#         if lparam==win32con.WM_LBUTTONDBLCLK:
#             self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
#         elif lparam==win32con.WM_RBUTTONUP:
#             self.show_menu()
#         elif lparam==win32con.WM_LBUTTONUP:
#             pass
#         return True

#     def show_menu(self):
#         menu = win32gui.CreatePopupMenu()
#         self.create_menu(menu, self.menu_options)
#         #win32gui.SetMenuDefaultItem(menu, 1000, 0)

#         pos = win32gui.GetCursorPos()
#         # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
#         win32gui.SetForegroundWindow(self.hwnd)
#         win32gui.TrackPopupMenu(menu,
#                                 win32con.TPM_LEFTALIGN,
#                                 pos[0],
#                                 pos[1],
#                                 0,
#                                 self.hwnd,
#                                 None)
#         win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

#     def create_menu(self, menu, menu_options):
#         for option_text, option_icon, option_action, option_id in menu_options[::-1]:
#             if option_icon:
#                 option_icon = self.prep_menu_icon(option_icon)

#             if option_id in self.menu_actions_by_id:                
#                 item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
#                                                                 hbmpItem=option_icon,
#                                                                 wID=option_id)
#                 win32gui.InsertMenuItem(menu, 0, 1, item)
#             else:
#                 submenu = win32gui.CreatePopupMenu()
#                 self.create_menu(submenu, option_action)
#                 item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
#                                                                 hbmpItem=option_icon,
#                                                                 hSubMenu=submenu)
#                 win32gui.InsertMenuItem(menu, 0, 1, item)

#     def prep_menu_icon(self, icon):
#         # First load the icon.
#         ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
#         ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
#         hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

#         hdcBitmap = win32gui.CreateCompatibleDC(0)
#         hdcScreen = win32gui.GetDC(0)
#         hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
#         hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
#         # Fill the background.
#         brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
#         win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
#         # unclear if brush needs to be feed.  Best clue I can find is:
#         # "GetSysColorBrush returns a cached brush instead of allocating a new
#         # one." - implies no DeleteObject
#         # draw the icon
#         win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
#         win32gui.SelectObject(hdcBitmap, hbmOld)
#         win32gui.DeleteDC(hdcBitmap)

#         return hbm

#     def command(self, hwnd, msg, wparam, lparam):
#         id = win32gui.LOWORD(wparam)
#         self.execute_menu_option(id)
#         return 0

#     def execute_menu_option(self, id):
#         menu_action = self.menu_actions_by_id[id]      
#         if menu_action == self.QUIT:
#             win32gui.DestroyWindow(self.hwnd)
#         else:
#             menu_action(self)

# def non_string_iterable(obj):
#     try:
#         iter(obj)
#     except TypeError:
#         return False
#     else:
#         return not isinstance(obj, str)

# # Minimal self test. You'll need a bunch of ICO files in the current working
# # directory in order for this to work...
# if __name__ == '__main__':
#     import asyncio
#     icon = os.path.join(BASE_DIR, "app", "assets", "icons", 'logo64.ico')
#     hover_text = "SysTrayIcon.py Demo"
#     def hello(sysTrayIcon): print("Hello World.")
#     def simon(sysTrayIcon): print("Hello Simon.")
    
#     menu_options = (('Say Hello', icon, hello),
#                     ('A sub-menu', icon, (('Say Hello to Simon', icon, simon),
#                                                  ))
#                    )
#     def bye(sysTrayIcon): print('Bye, then.')

#     SysTrayIcon(icon, hover_text, menu_options, on_quit=bye, default_menu_index=1)
