import pytest
import time
import requests
import sys
from index import Indexer
from utils import base_searcher


# put benchmarking in own file

# make method to diff all 4 methods
# run test against the entire index to check for errors
#
links = {
    "small": "https://www.gutenberg.org/files/11/11-0.txt",
    "medium": "https://www.gutenberg.org/files/2701/2701-0.txt",
    "large": "https://www.gutenberg.org/files/996/996-0.txt"
}


def GetText(site):
    response = requests.get(site)
    words = response.text.replace('\n', '')
    words = words.replace('\r', ' ').split(' ')
    return words

# GOAL TO PARAMETRIZE BIG DICT TESTS, BASE vs IND


# @pytest.fixture
# def alice_index(corpus):
#     CP = Indexer(corpus)
#     return CP


def diff_patterns(pat_1, pat_2):
    for i in pat_1:
        if i in pat_2:
            pat_2.pop(pat_2.index(i))

    return pat_2


def test_trinum():
    corpus = GetText(links['small'])
    index = Indexer(corpus)
    found_trinum = index.reindex()

    lens = [len(i) for i in corpus]
    t_nums = sum([(i * (i + 1)) / 2 for i in lens])

    assert t_nums == found_trinum


def test_accuracy():
    corpus = GetText(links['small'])
    counter = 0
    ind = Indexer(corpus)
    search_terms = list(ind.table.keys())
    mismatches = 0
    for i in search_terms:
        counter += 1
        i_vals = ind.search([i])[0]
        _, b_vals = base_searcher(corpus, [i])

        a = i_vals.copy()
        b = b_vals.copy()
        dif_ind_base = diff_patterns(a, b)

        mismatches += len(dif_ind_base)

    assert mismatches == 0





# For benchmarking V
# --------------------------------

# def test_index_speed(corpus):
#     start = time.time()
#     CP = Indexer(corpus)
#     finish = time.time() - start
#     size = sys.getsizeof(CP.table) * 1e-6
#     print('Indexing took {} seconds with size of {} mb'.format(
#         round(finish, 4),
#         size
#     ))

#     assert finish < .5
#     assert size < 3


# def benchmark_base(words, pattern):
#     pattern_words = []
#     start = time.time()
#     for word in words:
#         for pat in pattern:
#             if pat in word:
#                 pattern_words.append(word)
#     duration = time.time() - start
#     return duration, pattern_words


# def benchmark_index(index, pattern):
#     pattern_words = []
#     start = time.time()
#     words = index.search(pattern)
#     duration = time.time() - start
#     pattern_words = [i for j in words for i in j]
#     return duration, pattern_words


# def test_search_results_and_time(alice_index, corpus):
#     index = alice_index
#     corpus = corpus
#     base_time_pat_1, b_1 = benchmark_base(corpus, pattern_1)
#     base_time_pat_2, b_2 = benchmark_base(corpus, pattern_2)
#     base_time_pat_3, b_3 = benchmark_base(corpus, pattern_3)

#     index_time_pat_1, i_1 = benchmark_index(index, pattern_1)
#     index_time_pat_2, i_2 = benchmark_index(index, pattern_2)
#     index_time_pat_3, i_3 = benchmark_index(index, pattern_3)

#     diff_pat_1 = diff_patterns(b_1, i_1)
#     diff_pat_2 = diff_patterns(b_2, i_2)
#     diff_pat_3 = diff_patterns(b_3, i_3)

#     assert len(diff_pat_1) == 0
#     assert len(diff_pat_2) == 0
#     assert len(diff_pat_3) == 0

#     assert base_time_pat_1 > index_time_pat_1
#     assert base_time_pat_2 > index_time_pat_2
