# -*- coding: utf-8 -*-
import json
import re
from collections import defaultdict
from make_unicode import u

try:
    from urllib.request import urlopen

    def get(url):
        return list(map(u, urlopen(url).read().decode('utf-8').split('\n')))
except:
    from urllib2 import urlopen as get


def generate():
    url = 'http://www.unicode.org/Public/security/latest/confusables.txt'
    file = get(url)
    confusables_matrix = defaultdict(list)
    match = re.compile(r'[0-9A-F ]+\s+;\s*[0-9A-F ]+\s+;\s*\w+\s*#'
                       r'\*?\s*\( (.+) → (.+) \) (.+) → (.+)\t#',
                       re.UNICODE)
    for line in file:
        p = re.findall(match, line)
        if p:
            char1, char2, name1, name2 = p[0]
            confusables_matrix[char1].append({
                'c': char2,
                'n': name2,
            })
            confusables_matrix[char2].append({
                'c': char1,
                'n': name1,
            })

    confusables_matrix = dict(confusables_matrix)

    with open('confusables.json', 'w+') as datafile:
        json.dump(confusables_matrix, datafile)
    return True
