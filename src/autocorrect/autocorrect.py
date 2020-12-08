"""
Non-machine learning approach to an autocorrect function

Limitations:
Edits become exponential
No dependency on previous words (no tagging, markov, etc)


NEED TO FIND A CORPUS BECAUSE I DONT HAVE ONE
also i probably won't be able to find one for conversational speech (idk, bet, lmfao) but that's whatever. maybe i'll just add like 5000x counts of those words just so
that it will override other things, but that might mess up the algorithm for some. OR i just add one count of each, so that if i type it in it'll recognize it
"""

import re
import collections

def word_counts(txt):
    words = collections.Counter(
                    re.findall(r'\w+', open(txt).read().lower()))
    return words

words = word_counts('corpus.txt') #no need to normalize, this aint ML

def most_probable_edit(pruned_edits):
    return max(pruned_edits, key = lambda x: words[x])

def prune(edits):
    return set(e for e in edits if e in words)

def edit(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    poss_edits = set()
    for i in range(len(word)):
        left,right = word[:i],word[i:]
        poss_edits.add(left + right[1:]) #delete
        poss_edits |= set([left + w + right for w in letters]) #insert
        poss_edits |= set([left + w + right[1:] for w in letters]) #replace
        poss_edits |= set([left + right[1:i] + right[0] + right[i:] for j in range(2,len(right)+1)]) #switch (beginning char of right side with something else on right side)
    return poss_edits

def re_edit(words):
    edited = set()
    for w in words:
        edited |= edit(w)
    return edited

def autocorrect(word):
    if word in words:
        return word
    edits = edit(word)
    pruned_edits = prune(edits)
    edits = 0
    while len(pruned_edits) == 0 and edits < 2: #limiter so we don't mess up anything on infinite recursion (e.g. someone times in dol;ksfj:LSKJDFL:SKD:FLKJSDF)
        edits = re_edit(edits)
        pruned_edits = prune(edits)
    return word #couldn't find edit