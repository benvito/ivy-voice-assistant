import yaml
import threading
import logging
import os
import asyncio
import ctypes

from recognizer.speech_recognizer import SpeechRecognizerGoogle
from recognizer.command_recongnizer import CommandRecongitionModel, CommandRecongition
from commands.commands import CommandExecutor
from speech_synthesis.tts import TextToSpeech, LunaTTS
from config import BASE_DIR
from utils.audio import Audio, PvRecorderAudio
from recognizer.hotword import HotwordModel, PicoVoiceHotWord
from config.constants import WAKE_UP
from pvporcupine import PorcupineInvalidArgumentError

logging.basicConfig(level=logging.INFO, filename=os.path.join(BASE_DIR, 'logs', 'log.log'), filemode='w')


class Luna:
    __slots__ = ("recognizer", "hotword", "recorder", "cmd_recognizer", "active", "listen_to_command", "process_command", "luna_thread")
    def __init__(self):
        self.recognizer = None
        self.hotword = None
        self.recorder = None
        self.cmd_recognizer = None
        self.init()
        self.luna_thread = None
        self.active = True
        self.listen_to_command = False
        self.process_command = False
    def init_speech_recognizer(self):
        self.recognizer = SpeechRecognizerGoogle()

    def init_hotword(self):
        try:
            self.hotword = PicoVoiceHotWord()
        except PorcupineInvalidArgumentError as e:
            print(e.message)
            logging.warning(f"{e.message}")
            self.hotword = None

    def init_recorder(self):
        self.recorder = PvRecorderAudio()

    def init_command_recognizer(self):
        self.cmd_recognizer = CommandRecongition()
    
    def init_tts(self):
        LunaTTS.__init__(name="Anna", rate=150)

    def init(self):
        self.init_speech_recognizer()

        self.init_hotword()

        self.init_recorder()
        self.init_command_recognizer()
        self.init_tts()

    # @property
    # def active(self):
    #     return self._active
    
    # @active.setter
    # def active(self, value):
    #     self._active = value
    #     if value:
    #         self.start_loop()
    async def restart_loop(self):
        await self.stop_loop()
        if self.luna_thread.is_alive():
            self.emergency_stop_loop()
        await self.start_loop()
        print('Luna loop has been restarted')
    
    def wait_for_thread_finish(self):
        if self.luna_thread and self.luna_thread.is_alive():
            self.luna_thread.join()

    def emergency_stop_loop(self):
        thread_id = ctypes.c_long(self.luna_thread.ident)
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        self.wait_for_thread_finish()

    async def stop_loop(self):
        self.active = True
        # self.wait_for_thread_finish()

    async def start_loop(self):
        self.active = True
        self.luna_thread = threading.Thread(name="luna_thread", target=self.main_loop,
                                            daemon=True)
        self.luna_thread.start()

    def main_loop(self):
        

        # while True:
        # print(voice_input)
        # voice_input = "выключи компьютер через 50 минут"
        # voice_input = "не выключай комп"
        # voice_input = "сколько сейчас время"
        # voice_input = "Привет"
        # voice_input = "телеграм"
        # voice_input = "значение слова компьютер"
        # voice_input = "назови случайное число от пятьсот до пятьсот один"
        # voice_input = "громкость девяносто пять"
        # voice_input = "установи громкость на половину"
        # voice_input = "включи звук"
        # voice_input = "выключи звук"
        # voice_input = "пожалуйста умоляю подскажи время"
        # voice_input = "отключи от звонка в дискорде"
        # voice_input = "включи автопринятие в лиге легенд"
        # voice_input = "выключи автопринятие в лиге легенд"
        # voice_input = "переключи серию"
        # voice_input = "режим работа"
        # wait_for_name = rec.wait_for_name()

        # hotword = HotwordModel()
        # hotword.prepare_data()
        # hotword.train_model()
        # hotword.load_model()
        # Audio.record_audio_and_save(".", 1)
        # hotword.record_wake_audio_data(100, None)

        self.recorder.start()
        while self.active:
            # print("Listening...")
            try:
                frame = self.recorder.read()
                keyword_index = self.hotword.hotword_in_audio_frame(frame)
            except ValueError:
                pass
            if keyword_index != -1:
                wake_out = CommandExecutor.exec_nessesary_command(WAKE_UP, '')

                LunaTTS.say(wake_out)

                self.listen_to_command = True
                voice_input = self.recognizer.listen()
                self.process_command = True
                self.listen_to_command = False
                if voice_input:
                    print("voice_input: ", voice_input)
                    command_class = self.cmd_recognizer.recognize_command(voice_input)
                    print(command_class)
                    voice_output = CommandExecutor.exec_nessesary_command(command_class, voice_input)

                    print(voice_output)

                    LunaTTS.say(voice_output)
                self.process_command = False
        
        
        # while True:
        #     # print("Listening...")
        #     input_file = Audio.listen_for(seconds=1)
        #     if input_file is not None:
        #         wake_word = hotword.predict_hotword_in_file('input.wav')
        #         if wake_word:
        #             print("Wake word detected")
        #         else:
        #             print("Wake word NOT detected")
        # while True:
        #     pass
        #     print("Listening...")
        #     wait_for_name = rec.wait_for_name()
        #     if wait_for_name:
        #         voice_input = rec.listen(3)
        #         if voice_input:
        #             print("voice_input: ", voice_input)
        #             cr = CommandRecongition()
        #             command_class = cr.recognize_command(voice_input)
        #             print(command_class)
        #             voice_output = CommandExecutor.exec_nessesary_command(command_class, voice_input)

        #             print("voice_input: ", voice_input.split())
        #             print(voice_output)

        #             LunaTTS.say(voice_output)

        # voice_input = "выйди звонка в где скорби"
        # cr = CommandRecongition()
        # command_class = cr.recognize_command(voice_input)
        # print(command_class)

logging.shutdown()

