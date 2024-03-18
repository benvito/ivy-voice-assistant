# from num2words import num2words
# import torch as t
# import torchaudio
# import time
# from pydub import AudioSegment

# language = 'ru'
# model_id = 'v4_ru'
# sample_rate = 48000
# speaker = 'baya'
# put_accent = True
# put_yo = True
# device = t.device('cuda' if t.cuda.is_available() else 'cpu')

# text = "У меня вс+ё супер"

# # for word in text.split():
# #     if word.isdigit():
# #         text = text.replace(word, num2words(word, lang="ru"))

# model, _ = t.hub.load(repo_or_dir='snakers4/silero-models',
#                       model='silero_tts',
#                       language=language,
#                       speaker=model_id)


# model.to(device)

# audio = model.apply_tts(text=text,
#                         speaker=speaker,
#                         sample_rate=sample_rate,
#                         put_accent=put_accent,
#                         put_yo=put_yo)

# print(text)
# if audio.dim() == 1:
#     audio = audio.unsqueeze(0)
# torchaudio.save("audio.mp3", audio, sample_rate=44100)



