from text_to_num import alpha2digit
from num2words import num2words
import func as f
text = "установи громкость на 2.000"
text = text.replace(".", "")
text = f.num_to_word_in_string(text)
text = text.replace("млн", "миллион")
text = text.replace("млрд", "миллиард")
print(text)
text = alpha2digit(text, 'ru')
print(text)