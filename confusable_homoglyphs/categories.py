# -*- coding: utf-8 -*-
import json
import os
import re
from .make_unicode import u

try:
    from urllib.request import urlopen

    def get(url):
        return urlopen(url).read().decode('utf-8').split('\n')
except:
    from urllib2 import urlopen as get


def load():
    with open('{}/categories.json'.format(os.getcwd()), 'r') as file:
        return json.load(file)

try:
    categories_data = load()
except:
    try:
        from generate_categories import generate
        if generate():
            categories_data = load()
    except:
        raise Exception('Datafile not found, datafile generation failed!')


def aliases_categories(chr):
    l = 0
    r = len(categories_data['code_points_ranges']) - 1
    c = ord(chr)

    # binary search
    while r >= l:
        m = (l + r) // 2
        if c < categories_data['code_points_ranges'][m][0]:
            r = m - 1
        elif c > categories_data['code_points_ranges'][m][1]:
            l = m + 1
        else:
            return (
                categories_data['iso_15924_aliases'][categories_data['code_points_ranges'][m][2]],
                categories_data['categories'][categories_data['code_points_ranges'][m][3]])
    return 'Unknown', 'Zzzz'


def alias(chr):
    a, _ = aliases_categories(chr)
    return a


def category(chr):
    _, a = aliases_categories(chr)
    return a


def unique_aliases(string):
    cats = [alias(c) for c in string]
    return set(cats)


def delete():
    try:
        os.remove('{}/categories.json'.format(os.getcwd()))
    except OSError:
        pass


def generate():
    # inspired by https://gist.github.com/anonymous/2204527
    code_points_ranges = []
    iso_15924_aliases = []
    categories = []

    match = re.compile(r'([0-9A-F]+)(?:\.\.([0-9A-F]+))?\W+(\w+)\s*#\s*(\w+)',
                       re.UNICODE)

    url = 'http://www.unicode.org/Public/UNIDATA/Scripts.txt'
    file = get(url)
    for line in file:
        p = re.findall(match, line)
        if p:
            code_point_range_from, code_point_range_to, alias, category = p[0]
            alias = u(alias.upper())
            category = u(category)
            if alias not in iso_15924_aliases:
                iso_15924_aliases.append(alias)
            if category not in categories:
                categories.append(category)
            code_points_ranges.append((
                int(code_point_range_from, 16),
                int(code_point_range_to or code_point_range_from, 16),
                iso_15924_aliases.index(alias), categories.index(category))
            )
    code_points_ranges.sort()

    categories_data = {
        'iso_15924_aliases': iso_15924_aliases,
        'categories': categories,
        'code_points_ranges': code_points_ranges,
    }

    with open('{}/categories.json'.format(os.getcwd()), 'w+') as datafile:
        json.dump(categories_data, datafile)
    return True
