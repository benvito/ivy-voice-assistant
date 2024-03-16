import speech_recognition as sr
# from vosk import Model, KaldiRecognizer
from utils.yaml_utils import YamlData
from config.config import Config
from speech_synthesis.tts import LunaTTS
from config.constants import IO_DEVICES, INPUT_DEVICE, INDEX
import os
# import sounddevice as sd
import queue
import json
from utils.decorators import exec_timer


# class SpeechRecognizerVosk:
#     def __init__(self) -> None:
#         self.model = Model(os.path.join(".", "models", "vosk", "vosk-model-small-ru-0.22"))
#         self.recognizer = KaldiRecognizer(self.model,
#                                           16000)
#         self.q = queue.Queue()

#     def callback(self, indata, frames, time, status):
#         self.q.put(bytes(indata))

#     @exec_timer
#     def listen(self) -> str:
#         stream = sd.InputStream(callback=self.callback,
#                             samplerate=16000,
#                             blocksize=4000,
#                             device=1,
#                             channels=1,
#                             dtype='int16')
#         with stream:
#             try:
#                 while True:
#                     data = self.q.get()
#                     if self.recognizer.AcceptWaveform(data):
#                         res = self.recognizer.Result()
#                         print(res)
#                         return json.loads(res)['text']
#             except:
#                 pass

class SpeechRecognizerGoogle:
    def __init__(self) -> None:
        print(sr)
        self.current_microphone = Config.read_config()[IO_DEVICES][INPUT_DEVICE][INDEX]
        if self.current_microphone == -1:
            self.current_microphone = None
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=self.current_microphone)

    @exec_timer
    def listen(self, timeout : float = None) -> str:
        audio = None
        query = None
        with self.microphone as source:      
            print("DETECTING NOISES...") 
            self.recognizer.adjust_for_ambient_noise(source, 0.6)
            print("NOISES DETECTED")      
            while audio is None:
                if LunaTTS.saying_thread.is_alive() == False:
                    print("Listening...")
                    try:
                        audio = self.recognizer.listen(source, timeout=timeout)
                        if audio is not None:
                            query = self.recognize(audio)
                    except sr.UnknownValueError:
                        pass
                    except sr.WaitTimeoutError:
                        query = None
                        break
        return query

    @exec_timer
    def recognize(self, audio) -> str:
        query = None
        if audio:
            try:
                query = self.recognizer.recognize_google(audio_data=audio, language="ru-Ru").lower()
            except sr.UnknownValueError:
                pass

        return query

