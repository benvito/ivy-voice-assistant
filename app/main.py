import yaml
import threading
import logging
import os

from recognizer.speech_recognizer import SpeechRecognizerGoogle, SpeechRecognizerVosk
from recognizer.command_recongnizer import CommandRecongitionModel, CommandRecongition
from commands.commands import CommandExecutor
from speech_synthesis.tts import TextToSpeech
from utils import BASE_DIR

logging.basicConfig(level=logging.INFO, filename=os.path.join(BASE_DIR, 'logs', 'log.log'), filemode='w')

if __name__ == "__main__":
    rec = SpeechRecognizerGoogle()

    tts = TextToSpeech("Anna", 170)

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
    while True:
        print("Listening...")
        voice_input = rec.listen()
        if voice_input:
            print("voice_input: ", voice_input)
            cr = CommandRecongition()
            command_class = cr.recognize_command(voice_input)
            print(command_class)
            voice_output = CommandExecutor.exec_nessesary_command(command_class, voice_input)

            print("voice_input: ", voice_input.split())
            print(voice_output)

            tts.say(voice_output)

    # voice_input = "выйди звонка в где скорби"
    # cr = CommandRecongition()
    # command_class = cr.recognize_command(voice_input)
    # print(command_class)

