# -*- coding: utf-8 -*-
import pickle
import re
import urllib2
from collections import defaultdict


def generate():
    url = 'http://www.unicode.org/Public/security/latest/confusables.txt'
    file = urllib2.urlopen(url)
    confusables_matrix = defaultdict(list)
    match = re.compile(r'[0-9A-F ]+\s+;\s*[0-9A-F ]+\s+;\s*\w+\s*#'
                       r'\*?\s*\( (.+) → (.+) \) (.+) → (.+)\t#',
                       re.UNICODE)
    for line in file:
        p = re.findall(match, line)
        if p:
            char1, char2, name1, name2 = p[0]
            confusables_matrix[char1].append((char2, name2))
            confusables_matrix[char2].append((char1, name1))

    confusables_matrix = dict(confusables_matrix)

    with open('confusables.pkl', 'wb') as datafile:
        pickle.dump(confusables_matrix, datafile, 2)
    return confusables_matrix
