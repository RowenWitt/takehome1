import time
import re


def base_searcher(words, pattern):
    pattern_words = []
    start = time.time()
    for word in words:
        for pat in pattern:
            if pat in word:
                pattern_words.append(word)
    duration = time.time() - start
    return duration, pattern_words


def find_searcher(words, pattern):
    pattern_words = []
    start = time.time()
    for word in words:
        for pat in pattern:
            if word.find(pat) != -1:
                pattern_words.append(word)
    duration = time.time() - start
    return duration, pattern_words


def regex_searcher(words, pattern):
    pattern_words = []
    start = time.time()
    for word in words:
        for pat in pattern:
            if re.search(r'\{}'.format(pat), word):
                pattern_words.append(word)
    duration = time.time() - start
    return duration, pattern_words
