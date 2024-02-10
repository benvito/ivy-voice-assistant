import yaml
import threading

from recording import Recorder
from command_recongition import CommandRecongitionModel
from commands import CommandExecutor
from tts import TextToSpeech

class VoiceAssistant:
    name = ""
    sex = ""
    speech_recognition = ""
    recognition_language = ""


if __name__ == "__main__":
    rec = Recorder()

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
            cr = CommandRecongitionModel()
            command_class = cr.recognize_command(voice_input)
            print(command_class)
            voice_output = CommandExecutor.exec_nessesary_command(command_class, voice_input)

            print("voice_input: ", voice_input.split())
            print(voice_output)

            tts.say(voice_output)

