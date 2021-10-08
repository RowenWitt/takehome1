import requests
from index import Indexer
from utils import base_searcher


links = [
    "https://www.gutenberg.org/files/11/11-0.txt",
    "https://www.gutenberg.org/files/2701/2701-0.txt",
    "https://www.gutenberg.org/files/996/996-0.txt"
]


def get_text(site):
    ''' Requests and cleans books from
    Gutenberg website '''
    response = requests.get(site)
    words = response.text.replace('\n', '')
    words = words.replace('\r', ' ').split(' ')
    return words


def diff_patterns(pat_1, pat_2):
    ''' Compares two lists, output will
    have length of 0 if no difference '''
    for i in pat_1:
        if i in pat_2:
            pat_2.pop(pat_2.index(i))

    return pat_2


def test_trinum():
    ''' Compares the number of steps made
    while reindexing, to the sum of the
    triangular number of the length of each
    string.  This equation tells you how many
    subgroups can be found in a string
        Xn = n(n + 1) / 2 '''
    corpus = get_text(links[0])
    index = Indexer(corpus)
    found_trinum = index.reindex()

    lens = [len(i) for i in corpus]
    t_nums = sum([(i * (i + 1)) / 2 for i in lens])

    assert t_nums == found_trinum


def test_accuracy(per=100):
    ''' Compares the results of the index search
    to the example searcher.  The search terms are
    the keys of the index storing the list data.
    The per keyword determines the frequency of comparison.
    per of 100 means every 100th key term is being compared.
    There are 60,000 keys in the alice in wonderland index. '''
    corpus = get_text(links[0])
    ind = Indexer(corpus)
    search_terms = list(ind.table.keys())
    mismatches = 0
    for i in range(len(search_terms)):
        if i % per == 0:
            i_vals = ind.search([search_terms[i]])[0]
            _, b_vals = base_searcher(corpus, [search_terms[i]])

            a = i_vals.copy()
            b = b_vals.copy()
            dif_ind_base = diff_patterns(a, b)

            mismatches += len(dif_ind_base)

    assert mismatches == 0


def index_speed(corpus):
    index = Indexer(corpus)
    return index


def test_index_speeds_small(benchmark):
    ''' Tests index speed on 40k word
    Alice in wonderland corpus '''
    corpus = get_text(links[0])
    val = benchmark(index_speed, corpus)
    assert len(val.table) != 0


def test_index_speeds_medium(benchmark):
    ''' Test index speed on 200k word
    Moby Dick Corpus '''
    corpus = get_text(links[1])
    val = benchmark(index_speed, corpus)
    assert len(val.table) != 0
