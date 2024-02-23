import yaml
import threading
import logging
import os
import asyncio

from recognizer.speech_recognizer import SpeechRecognizerGoogle
from recognizer.command_recongnizer import CommandRecongitionModel, CommandRecongition
from commands.commands import CommandExecutor
from speech_synthesis.tts import TextToSpeech, LunaTTS
from config import BASE_DIR
from utils.audio import Audio, PvRecorderAudio
from recognizer.hotword import HotwordModel, PicoVoiceHotWord
from config.constants import WAKE_UP

logging.basicConfig(level=logging.INFO, filename=os.path.join(BASE_DIR, 'logs', 'log.log'), filemode='w')

if __name__ == "__main__":
    rec = SpeechRecognizerGoogle()

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


    hotword = PicoVoiceHotWord()
    recorder = PvRecorderAudio()
    recorder.start()
    while True:
        frame = recorder.read()
        keyword_index = hotword.hotword_in_audio_frame(frame)
        if keyword_index != -1:
            wake_out = CommandExecutor.exec_nessesary_command(WAKE_UP, '')
            LunaTTS.say(wake_out)
            voice_input = rec.listen()
            if voice_input:
                print("voice_input: ", voice_input)
                cr = CommandRecongition()
                command_class = cr.recognize_command(voice_input)
                print(command_class)
                voice_output = CommandExecutor.exec_nessesary_command(command_class, voice_input)

                print(voice_output)

                LunaTTS.say(voice_output)
    
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

