import func as f
import speech_recognition
import recording as rec
import pyttsx3
import yaml
import command_recongition as cr
import commands

class VoiceAssistant:
    name = ""
    sex = ""
    speech_recognition = ""
    recognition_language = ""


if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()

    ttsEngine = pyttsx3.init()
    voices = ttsEngine.getProperty("voices")
    for voice in range(len(voices)):
        if voices[voice].name == "Anna":
            ttsEngine.setProperty("voice", voices[voice].id)
            ttsEngine.setProperty("rate", 150)


    # while True:
    print('Listening...')
    # voice_input = rec.record_and_recognize(recognizer, mic)
    # print(voice_input)
    voice_input = "выключи компьютер через два часа и тридцать пять минут"
    # voice_input = "сколько сейчас время"
    
    command_class = cr.recognize_command(voice_input)
    voice_output = commands.exec_nessesary_command(command_class, voice_input)

    print(voice_input)
    print(voice_output)
    ttsEngine.say(voice_output)
    ttsEngine.runAndWait()
