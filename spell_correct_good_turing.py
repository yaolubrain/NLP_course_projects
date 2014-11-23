import numpy as np
import string, glob, sys
from collections import Counter

alphabet = string.ascii_lowercase

deletion_table_file = '/home/yao/Code/ConfusionTables/deletiontable.csv'
insertion_table_file = '/home/yao/Code/ConfusionTables/insertionstable.csv'
substitution_table_file = '/home/yao/Code/ConfusionTables/substitutionstable.csv'
reversal_table_file = '/home/yao/Code/ConfusionTables/transpositionstable.csv'

deletion_table = np.genfromtxt(deletion_table_file, delimiter=',')
insertion_table = np.genfromtxt(insertion_table_file, delimiter=',')
substitution_table = np.genfromtxt(substitution_table_file, delimiter=',')
reversal_table = np.genfromtxt(reversal_table_file, delimiter=',')

deletion_table = np.delete(np.delete(deletion_table, 0, axis=0), 0, axis=1)
insertion_table = np.delete(np.delete(insertion_table, 0, axis=0), 0, axis=1)
substitution_table = np.delete(np.delete(substitution_table, 0, axis=0), 0, axis=1)
reversal_table = np.delete(np.delete(reversal_table, 0, axis=0), 0, axis=1)

char2idx = dict((char, ord(char) - ord('a')) for char in alphabet)
char2idx[''] = 26

def smooth(X):
    unique, counts = np.unique(X, return_counts=True)
    freq = dict(zip(unique, counts)) 
    Y = np.zeros_like(X) 
    for i in xrange(X.shape[0]):
        for j in xrange(X.shape[1]):
            if X[i,j]+1 in freq:
                Y[i,j] = (X[i,j]+1)*freq[X[i,j]+1] / freq[X[i,j]] 
            else:
                Y[i,j] = 0
    return Y

deletion_table = smooth(deletion_table)
insertion_table = smooth(insertion_table)
substitution_table = smooth(substitution_table)
reversal_table = smooth(reversal_table)


def Del(x, y):
    return deletion_table[char2idx[x],char2idx[y]]

def Add(x, y):
    return insertion_table[char2idx[x],char2idx[y]]

def Sub(x, y):
    return substitution_table[char2idx[x],char2idx[y]]

def Rev(x, y):
    return reversal_table[char2idx[x],char2idx[y]]


all_words_file = ['/home/yao/Downloads/NLP/spell_correction/english.0',
                  '/home/yao/Downloads/NLP/spell_correction/english.1',
                  '/home/yao/Downloads/NLP/spell_correction/english.2',
                  '/home/yao/Downloads/NLP/spell_correction/english.3']
all_words = []
for file in all_words_file:
    with open(file) as f:
        words = f.read().split()
        all_words += ([w.split('/')[0] for w in words])

all_words = set(all_words)


all_words_join = ' '.join(all_words)
chars_x  = dict((x, all_words_join.count(x)) for x in alphabet)
chars_xy = dict((x+y, all_words_join.count(x+y)) for x in alphabet for y in alphabet)
chars = dict(chars_x.items() + chars_xy.items())

freq = Counter()
for file in glob.glob("/home/yao/Downloads/NLP/spell_correction/ap8802*"):
    with open(file) as f:
        freq += Counter(f.read().split())

def Prob(word, x, y, trans):
    if trans == 'deletion':
        return (freq[word]+0.5)/sum(freq.values())*(Del(x, y)/chars[x+y])
    elif trans == 'insertion':
        return (freq[word]+0.5)/sum(freq.values())*(Add(x, y)/chars[x])
    elif trans == 'substitution':
        return (freq[word]+0.5)/sum(freq.values())*(Sub(x, y)/chars[y])
    elif trans == 'reversal':
        return (freq[word]+0.5)/sum(freq.values())*(Rev(x, y)/chars[x+y])

def Deletions(word):
    splits  = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [(a+b[1:], Prob(a+b[1:], a[-1], b[0], 'deletion'))
               for a, b in splits if b and a+b[i:] in all_words]
    return deletes

def Insertions(word):
    splits  = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    inserts = [(a+c+b, Prob(a+c+b, a[-1], c, 'insertion'))
               for a, b in splits for c in alphabet if a+c+b in all_words]
    return inserts

def Substitutions(word):
    splits  = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    substitutes = [(a+c+b[1:], Prob(a+c+b[1:], b[0], c, 'substitution'))
                   for a, b in splits for c in alphabet if b and a+c+b[1:] in all_words]
    return substitutes

def Reversals(word):
    splits  = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    reversals = [(a+b[1]+b[0]+b[2:], Prob(a+b[1]+b[0]+b[2:], b[0], b[1], 'reversal'))
                 for a, b in splits if len(b)>1 and a+b[1]+b[0]+b[2:] in all_words]
    return reversals

def Correct(word):
    corrections = Deletions(word) + Insertions(word) + Substitutions(word) + Reversals(word)
    return sorted(corrections, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    words = sys.argv[1:]
    for word in words:
        corr = Correct(word)
        for c in corr:
            print c[0],

