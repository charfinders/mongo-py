import collections
import re

URL = 'http://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt'


Character = collections.namedtuple('Character', 'char name')


def tokenize(name):
    return re.split('\W+', name)


def parse(line):
    parts = line.split(';')
    name = parts[1]
    name_words = set(tokenize(name))
    if parts[10] and any(w not in name_words for w in tokenize(parts[10])):
        name += ' | ' + parts[10]
    return Character(chr(int(parts[0], 16)), name)
