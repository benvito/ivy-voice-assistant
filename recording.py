import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import os
import sounddevice as sd
import queue
import json
from decorators import exec_timer


class Recorder:
    def __init__(self) -> None:
        self.model = Model(os.path.join(".", "models", "vosk", "vosk-model-small-ru-0.22"))
        self.recognizer = KaldiRecognizer(self.model,
                                          16000)
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    @exec_timer
    def listen(self) -> str:
        stream = sd.InputStream(callback=self.callback,
                            samplerate=16000,
                            blocksize=4000,
                            device=1,
                            channels=1,
                            dtype='int16')
        with stream:
            try:
                while True:
                    data = self.q.get()
                    if self.recognizer.AcceptWaveform(data):
                        res = self.recognizer.Result()
                        print(res)
                        return json.loads(res)['text']
            except:
                pass

# class Recorder:
#     def __init__(self) -> None:
#         self.recognizer = sr.Recognizer()
#         self.microphone = sr.Microphone()

#     @exec_timer
#     def listen(self) -> str:
#         audio = None
#         with self.microphone as source:
#             self.recognizer.adjust_for_ambient_noise(source)
#             while audio is None:
#                 try:
#                     audio = self.recognizer.listen(source, timeout=None)
#                 except sr.UnknownValueError:
#                     pass
#         return audio

#     @exec_timer
#     def recognize(self, audio) -> str:
#         query = None
#         if audio:
#             try:
#                 query = self.recognizer.recognize_google(audio_data=audio, language="ru-Ru").lower()
#             except sr.UnknownValueError:
#                 pass

#         return query

