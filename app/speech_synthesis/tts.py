import pyttsx3
import asyncio
import threading
import sys
import time
import os
import asyncio
from utils.audio import Audio
from config.config import Config
from config.constants import IO_DEVICES, OUTPUT_DEVICE, INDEX
from config import TEMP_PATH
from equalizer import Equalizer



class TextToSpeech(pyttsx3.Engine):
    def __init__(
            self, 
            name : str, 
            rate : int,
            answer_file_name : str = os.path.join(TEMP_PATH, 'luna_answer.mp3')
            ) -> pyttsx3.Engine:
        super().__init__()
        self.answer_file_name = answer_file_name
        self.name = name
        self.rate = rate
        self.output_device = Config.read_config()[IO_DEVICES][OUTPUT_DEVICE][INDEX]
        self.saying_thread = threading.Thread()
        
        global ttsEngine
        ttsEngine = pyttsx3.init()
        voices = ttsEngine.getProperty("voices")
        for voice in range(len(voices)):
            if voices[voice].name == self.name:
                ttsEngine.setProperty("voice", voices[voice].id)
                ttsEngine.setProperty("rate", self.rate)
                break
    
    @property
    def equalizer(self):
        return self._equalizer
    
    @equalizer.setter
    def equalizer(self, value : Equalizer):
        self._equalizer = value

    def update_output_device(self):
        self.output_device = Config.read_config()[IO_DEVICES][OUTPUT_DEVICE][INDEX]
    
    def say(self, text : str):
        self.saying_thread = threading.Thread(name="TTS", target=self.say_thread_task, args=(text, ))
        self.saying_thread.daemon = True
        self.saying_thread.start()


    def say_thread_task(self, text : str):
        global ttsEngine
        if text:
            if ttsEngine._inLoop:
                ttsEngine.endLoop()
            path_to_answer = self.answer_file_name
            print(path_to_answer)
            if os.path.exists(path_to_answer):
                os.remove(path_to_answer)
            ttsEngine.save_to_file(text, path_to_answer)
            ttsEngine.runAndWait()

            if os.path.exists(path_to_answer):
                Audio.play_mono_audio(path_to_answer, self.output_device, equalizer=self.equalizer)
                # os.remove(path_to_answer)

LunaTTS = TextToSpeech(name="Anna", rate=150)

