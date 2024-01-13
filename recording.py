import speech_recognition as sr

def record_and_recognize(recognizer : sr.Recognizer, mic : sr.Microphone) -> str:
    query = ""
    with mic:
        recognizer.adjust_for_ambient_noise(source=mic, duration=0.5)
        try:
            audio = recognizer.listen(source=mic)
        except sr.WaitTimeoutError:
            print("Waiting too much...")
        
    try:
        query = recognizer.recognize_google(audio_data=audio, language="ru-Ru").lower()
    except sr.UnknownValueError:
        pass
    return query