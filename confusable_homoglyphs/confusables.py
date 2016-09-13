# -*- coding: utf-8 -*-
import json
import os
import re
from collections import defaultdict
from make_unicode import u
import categories

try:
    from urllib.request import urlopen

    def get(url):
        return list(map(u, urlopen(url).read().decode('utf-8').split('\n')))
except:
    from urllib2 import urlopen as get


def load():
    with open('{}/confusables.json'.format(os.getcwd()), 'r') as file:
        return json.load(file)

try:
    confusables_data = load()
except:
    try:
        from generate_confusables import generate
        if generate():
            confusables_data = load()
    except:
        raise Exception('Datafile not found, datafile generation failed!')


def is_mixed_script(string, allowed_categories=['COMMON']):
    allowed_categories = map(str.upper, allowed_categories)
    cats = categories.unique_aliases(string) - set(allowed_categories)
    return len(cats) > 1


def is_confusable(string, greedy=False, preferred_aliases=[]):
    preferred_aliases = list(map(str.upper, preferred_aliases))
    outputs = []
    checked = set()
    for char in string:
        if char in checked:
            continue
        checked.add(char)
        alias = categories.alias(char)
        if alias in preferred_aliases:
            # these are safe: the character is confusable with homoglyphs from other
            # categories than our preferred categories (=aliases)
            continue
        found = confusables_data.get(char)
        if found:  # we found homoglyphs
            output = {
                'character': char,
                'alias': alias,
                'homoglyphs': found,
            }
            if not greedy:
                return [output]
            outputs.append(output)

    return outputs or False


def is_dangerous(string, preferred_aliases=[]):
    return is_mixed_script(string) and is_confusable(string, *preferred_aliases)


def delete():
    try:
        os.remove('{}/confusables.json'.format(os.getcwd()))
    except OSError:
        pass


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

    with open('{}/confusables.json'.format(os.getcwd()), 'w+') as datafile:
        json.dump(confusables_matrix, datafile)
    return True
