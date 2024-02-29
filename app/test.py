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
