# -*- coding: utf-8 -*-
import re
from collections import defaultdict

from .utils import u, get, dump

try:
    import click
except ImportError:
    print('Install this package with the [cli] extras to enable the CLI.')
    raise


@click.group()
def cli():
    pass


@cli.command()
def update():
    """
    Update the homoglyph data files from https://www.unicode.org
    """
    generate_categories()
    generate_confusables()


def generate_categories():
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

    dump('categories.json', categories_data)


def generate_confusables():
    """Generates the confusables JSON data file from the unicode specification.

    :return: True for success, raises otherwise.
    :rtype: bool
    """
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

    dump('confusables.json', dict(confusables_matrix))
