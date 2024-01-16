import pyttsx3

def init(name : str, rate : int) -> pyttsx3.Engine:
    global ttsEngine
    ttsEngine = pyttsx3.init()
    voices = ttsEngine.getProperty("voices")
    for voice in range(len(voices)):
        if voices[voice].name == name:
            ttsEngine.setProperty("voice", voices[voice].id)
            ttsEngine.setProperty("rate", rate)
            break
    return ttsEngine

def say(text : str):
    ttsEngine.say(text)
    ttsEngine.runAndWait()