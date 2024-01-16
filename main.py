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

    tts.init("Anna", 160)

    # while True:
    print('Listening...')
    # voice_input = rec.record_and_recognize(recognizer, mic)
    # print(voice_input)
    # voice_input = "выключи компьютер через два часа"
    voice_input = "не выключай комп"
    # voice_input = "сколько сейчас время"
    
    command_class = cr.recognize_command(voice_input)
    voice_output = commands.exec_nessesary_command(command_class, voice_input)

    print(voice_input)
    print(voice_output)

    tts.say(voice_output)
