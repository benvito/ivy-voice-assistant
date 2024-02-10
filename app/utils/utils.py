from pymorphy3 import MorphAnalyzer
from fuzzywuzzy import fuzz
from num2words import num2words
from text_to_num import alpha2digit
import time
import re
import os
import yaml
from functools import lru_cache

from config.config import SECOND_TO_NANO, TIME_DELIMITER, WORD_MATCH_RATIO
from utils.decorators import exec_timer

class StringProcessing:
    @staticmethod
    @exec_timer
    def remove_brackets(text):
        pattern = r'\([^()]*\)'
        while re.search(pattern, text):
            text = re.sub(pattern, '', text)
        return text

    @staticmethod
    def list_to_string(list: list) -> str:
        return ' '.join(list)

    @staticmethod
    def contains_substring(list_of_strings, substring):
        return any(substring in s for s in list_of_strings)


class Time:
    @staticmethod
    def is_hour(word):
        return word == 'час' or \
                word == 'часа' or \
                word == 'часов' or \
                word == 'часик' or \
                word == 'часика' or \
                word == 'часиков'

    @staticmethod
    def is_minute(word):
        return word == 'минута' or \
                word == 'минут' or \
                word == 'минуты' or \
                word == 'минуток' or \
                word == 'минутки' or \
                word == 'минутку'

    @staticmethod
    def is_second(word):
        return word == 'секунда' or \
                word == 'секунд' or \
                word == 'секунды' or \
                word == 'секундок' or \
                word == 'секундочек' or \
                word == 'секундочку' or \
                word == 'секундочки'

    @staticmethod
    def convert_to_seconds(time : any) -> int:
        time_in_seconds = 0
        for arg in time:
            if Time.is_hour(arg[-1]):
                time_in_seconds += int(arg[0]) * 3600
            elif Time.is_minute(arg[-1]):
                time_in_seconds += int(arg[0]) * 60
            elif Time.is_second(arg[-1]):
                time_in_seconds += int(arg[0])
        return time_in_seconds

    @staticmethod
    def convert_to_nanoseconds(re_arguments):
        result = Time.convert_to_seconds(re_arguments)
        result = result * SECOND_TO_NANO
        return result

    @staticmethod
    @exec_timer
    def time_format_for_string(text: str) -> str:
        time_part = ''
        time_delim = ':'

        for i in range(len(text)):
            if text[i] in TIME_DELIMITER:
                time_delim = text[i]
                if text[i-2].isdigit():
                    time_part += text[i-2]
                time_part += text[i-1:i+1]
                if text[i+1].isdigit():
                    time_part += text[i+1:i+3]
                if text[i+3] in TIME_DELIMITER:
                    time_part += text[i+3:i+5]
                break

        time_part = time_part.split(time_delim)

        time_words = ['час', 'минута', 'секунда']

        time_result_string = ''

        for i in range(len(time_part)):
            if time_part[i].isdigit():
                inflected_time_word = WordNum.inflect_word_with_count(time_words[i], int(time_part[i]))
                time_result_string += time_part[i] + ' ' + inflected_time_word
            if i != len(time_part) - 1:
                time_result_string += ' '

        return time_result_string


class WordNum:
    """
    ALL ABOUT RELATIONS WITH WORDS AND NUMBERS 
    """

    @staticmethod
    @exec_timer
    def word_to_num_in_string(text : str) -> str:
        text = alpha2digit(text, 'ru')
        return text

    @staticmethod
    def num_to_word_in_string(text : str) -> str:
        if not text:
            return None
        for word in text.split():
            if word.isdigit():
                text = text.replace(word, num2words(word, lang="ru"))
        return text

    @staticmethod
    @exec_timer
    def inflect_word_with_count(word : str, count : int) -> str:
        morph = MorphAnalyzer()
        morph_word = morph.parse(word)[0]
        inflected_word = morph_word.make_agree_with_number(count).word
        return inflected_word

def word_is_in_list(word : str, text : list) -> int:
    for i in range(len(text)):
        if is_this_word(text[i], word):
            return i
    return -1

def diff_words(word1 : str, word2 : str) -> float:
    return fuzz.token_sort_ratio(word1.lower(), word2.lower())
    
def is_this_word(word_predicted : str, word_expected : str) -> bool:
    ratio = diff_words(word_predicted, word_expected)
    if ratio >= WORD_MATCH_RATIO * 100:
        return True
    return False

def round_word_by_similarity(word_predicted : str, word_expected : str) -> str:
    ratio = diff_words(word_predicted, word_expected)
    if ratio >= WORD_MATCH_RATIO * 100:
        return word_expected
    else:
        return word_predicted

def pick_word_from_list_by_similarity(word : str, word_list : any) -> str:
    max_ratio = 0
    max_word = ''
    for w in word_list:
        ratio = diff_words(word, w)
        # print(word, w, ' - ', ratio)
        if ratio > max_ratio and ratio >= WORD_MATCH_RATIO * 100:
            max_ratio = ratio
            max_word = w
    # print("-------------------")    
    # if not max_word:
    #     word_determinated = determ_word(word)
    #     for w in word_list:
    #         ratio = diff_words(word_determinated, w)
    #         print(word_determinated, w, ' - ', ratio)
    #         if ratio > max_ratio and ratio >= WORD_MATCH_RATIO:
    #             max_ratio = ratio
    #             max_word = w

    if not max_word:
        max_word = word
    return max_word


def query_to_list(query):
    query = query.lower()
    return query.split(' ')

@exec_timer
def determ_query(query):
    for i in range(len(query)):
        query[i] = determ_word(query[i])
    return query


# @lru_cache(maxsize=128)
def determ_word(word):
    m = MorphAnalyzer()
    
    try:
        word = m.parse(word)[0]
        lemma = word.normal_form
        return lemma
    except IndexError:
        return word
    except Exception as e: 
        print(f'Error: {e}')
        return word

    # m = pymystem3.Mystem()
    # analysis = m.analyze(word)

    # try:
    #     return analysis[0]['analysis'][0]['lex']
    # except IndexError:
    #     return word
    # except Exception as e: 
    #     print(f'Error: {e}')
    #     return word