import func as f
import phrases as phr
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


    while True:
        voice_input = rec.record_and_recognize(recognizer, mic)
        
        command_type = cr.recognize_command(voice_input)
        exec("commands." + command_type + "(voice_input)")
        init_voice_input = voice_input
        voice_input = f.query_to_list(voice_input)

        print(voice_input)
        ttsEngine.say("".join(voice_input))
        ttsEngine.runAndWait()