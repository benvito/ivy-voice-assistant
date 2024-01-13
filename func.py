from pymorphy2 import MorphAnalyzer
from fuzzywuzzy import fuzz

WORD_MATCH_RATIO = 80


def word_is_in_list(word : str, text : list) -> int:
    for i in range(len(text)):
        if is_this_word(text[i], word):
            return i
    return -1

def diff_words(word1 : str, word2 : str) -> float:
    return fuzz.token_sort_ratio(word1.lower(), word2.lower())

def round_word_by_similarity(word_predicted : str, word_expected : str) -> str:
    ratio = diff_words(word_predicted, word_expected)
    if ratio >= WORD_MATCH_RATIO:
        return word_expected
    else:
        return word_predicted
    
def is_this_word(word_predicted : str, word_expected : str) -> bool:
    ratio = diff_words(word_predicted, word_expected)
    print(word_predicted, word_expected, ' - ', ratio)
    if ratio >= WORD_MATCH_RATIO:
        return True
    # else:
    #     ratio = diff_words(determ_word(word_predicted), word_expected)
    #     if ratio >= WORD_MATCH_RATIO:
    #         print(determ_word(word_predicted), word_expected, ' - ', ratio)
    #         return True
    
    return False

def pick_word_from_list_by_similarity(word : str, word_list : list or set) -> str:
    max_ratio = 0
    max_word = ''
    for w in word_list:
        ratio = diff_words(word, w)
        # print(word, w, ' - ', ratio)
        if ratio > max_ratio and ratio >= WORD_MATCH_RATIO:
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

def determ_query(query):
    for i in range(len(query)):
        query[i] = determ_word(query[i])
    return query

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