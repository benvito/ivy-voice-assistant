from num2words import num2words
import torch as t
import sounddevice as sd
import time

language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'baya'
put_accent = True
put_yo = True
device = t.device('cuda' if t.cuda.is_available() else 'cpu')

text = "Текущее время на часах хуй знает"

for word in text.split():
    if word.isdigit():
        text = text.replace(word, num2words(word, lang="ru"))

model, _ = t.hub.load(repo_or_dir='snakers4/silero-models',
                      model='silero_tts',
                      language=language,
                      speaker=model_id)


model.to(device)

audio = model.apply_tts(text=text,
                        speaker=speaker,
                        sample_rate=sample_rate,
                        put_accent=put_accent,
                        put_yo=put_yo)

print(text)

sd.play(audio, sample_rate)
time.sleep(len(audio) / sample_rate)
sd.stop()


