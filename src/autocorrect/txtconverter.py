import re
import collections
import pickle

def word_counts(txt):
    words = collections.Counter(
        re.findall(r'\w+', open(txt).read().lower()))
    return words


words = word_counts('corpus.txt')  # no need to normalize, this aint ML

with open('corpus_counter.pickle', 'wb') as pick:
    pickle.dump(words, pick)