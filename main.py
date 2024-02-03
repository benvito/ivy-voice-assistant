import speech_recognition
import yaml

import func as f
import recording as rec
import command_recongition as cr
import commands
import tts

class VoiceAssistant:
    name = ""
    sex = ""
    speech_recognition = ""
    recognition_language = ""


if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()

    tts.init("Anna", 170)

    # while True:
    print('Listening...')
    # voice_input = rec.record_and_recognize(recognizer, mic)
    # print(voice_input)
    # voice_input = "выключи компьютер через 2 часа 5 минут"
    # voice_input = "не выключай комп"
    # voice_input = "сколько сейчас время"
    # voice_input = "Привет"
    voice_input = "телеграм"
    # voice_input = "значение слова компьютер"
    # voice_input = "назови случайное число от пятьсот до пятьсот один"
    # voice_input = "громкость девяносто пять"
    # voice_input = "установи громкость на половину"
    # voice_input = "включи звук"
    # voice_input = "пожалуйста умоляю подскажи время"
    # voice_input = "отключи от звонка в дискорде"
    # voice_input = "включи автопринятие в лиге легенд"
    voice_input = "переключи серию"
    
    command_class = cr.recognize_command(voice_input)
    print(command_class)
    voice_output = commands.exec_nessesary_command(command_class, voice_input)

    print("voice_input: ", voice_input.split())
    print(voice_output)

    tts.say(voice_output)

