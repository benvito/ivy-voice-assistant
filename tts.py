import pyttsx3

class TextToSpeech(pyttsx3.Engine):
    def __init__(self, name : str, rate : int) -> pyttsx3.Engine:
        super().__init__()
        self.name = name
        self.rate = rate
        global ttsEngine
        ttsEngine = pyttsx3.init()
        voices = ttsEngine.getProperty("voices")
        for voice in range(len(voices)):
            if voices[voice].name == self.name:
                ttsEngine.setProperty("voice", voices[voice].id)
                ttsEngine.setProperty("rate", self.rate)
                break
    
    @staticmethod
    def say(text : str):
        global ttsEngine
        if text:
            ttsEngine.say(text)
            ttsEngine.runAndWait()