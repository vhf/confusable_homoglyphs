# -*- coding: utf-8 -*-
import json
import os
import re
from .utils import u, get, load


def aliases_categories(chr):
    """Retrieves the script block alias and unicode category for a unicode character.

    >>> categories.aliases_categories('A')
    ('LATIN', 'L')
    >>> categories.aliases_categories('τ')
    ('GREEK', 'L')
    >>> categories.aliases_categories('-')
    ('COMMON', 'Pd')

    :param chr: A unicode character
    :type chr: str
    :return: The script block alias and unicode category for a unicode character.
    :rtype: (str, str)
    """
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
    """Retrieves the script block alias for a unicode character.

    >>> categories.alias('A')
    'LATIN'
    >>> categories.alias('τ')
    'GREEK'
    >>> categories.alias('-')
    'COMMON'

    :param chr: A unicode character
    :type chr: str
    :return: The script block alias.
    :rtype: str
    """
    a, _ = aliases_categories(chr)
    return a


def category(chr):
    """Retrieves the unicode category for a unicode character.

    >>> categories.category('A')
    'L'
    >>> categories.category('τ')
    'L'
    >>> categories.category('-')
    'Pd'

    :param chr: A unicode character
    :type chr: str
    :return: The unicode category for a unicode character.
    :rtype: str
    """
    _, a = aliases_categories(chr)
    return a


def unique_aliases(string):
    """Retrieves all unique script block aliases used in a unicode string.

    >>> categories.unique_aliases('ABC')
    {'LATIN'}
    >>> categories.unique_aliases('ρAτ-')
    {'GREEK', 'LATIN', 'COMMON'}

    :param string: A unicode character
    :type string: str
    :return: A set of the script block aliases used in a unicode string.
    :rtype: (str, str)
    """
    cats = [alias(c) for c in string]
    return set(cats)


def generate():
    """Generates the categories JSON data file from the unicode specification.

    :return: True for success, raises otherwise.
    :rtype: bool
    """
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


try:
    categories_data = load('categories.json')
except:
    try:
        if generate():
            categories_data = load('categories.json')
    except:
        raise Exception('Datafile not found, datafile generation failed!')
