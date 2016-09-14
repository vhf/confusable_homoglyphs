# -*- coding: utf-8 -*-
import json
import os
import re
from collections import defaultdict
from .utils import get, load
from .categories import unique_aliases, alias


def is_mixed_script(string, allowed_categories=['COMMON']):
    """Checks if ``string`` contains mixed-scripts content, excluding script
    blocks aliases in ``allowed_categories``.

    E.g. ``B. C`` is not considered mixed-scripts by default: it contains characters
    from **Latin** and **Common**, but **Common** is excluded by default.

    :param string: A unicode string
    :type string: str
    :param allowed_categories: Script blocks aliases not to consider.
    :type allowed_categories: list(str)
    :return: Whether ``string`` is considered mixed-scripts or not.
    :rtype: bool
    """
    allowed_categories = map(str.upper, allowed_categories)
    cats = unique_aliases(string) - set(allowed_categories)
    return len(cats) > 1


def is_confusable(string, greedy=False, preferred_aliases=[]):
    """Checks if ``string`` contains characters which might be confusable with
    characters from ``preferred_aliases``.

    If ``greedy=False``, it will only return the first confusable character
    found without looking at the rest of the string, ``greedy=True`` returns
    all of them.

    ``preferred_aliases=[]`` can take an array of unicode block aliases to
    be considered as your 'base' unicode blocks:

    -  considering ``paρa``,

       -  with ``preferred_aliases=['latin']``, the 3rd character ``ρ``
          would be returned because this greek letter can be confused with
          latin ``p``.
       -  with ``preferred_aliases=['greek']``, the 1st character ``p``
          would be returned because this latin letter can be confused with
          greek ``ρ``.
       -  with ``preferred_aliases=[]`` and ``greedy=True``, you'll discover
          the 29 characters that can be confused with ``p``, the 23
          characters that look like ``a``, and the one that looks like ``ρ``
          (which is, of course, *p* aka *LATIN SMALL LETTER P*).

    :param string: A unicode string
    :type string: str
    :param greedy: Don't stop on finding one confusable character - find all of them.
    :type greedy: bool
    :param preferred_aliases: Script blocks aliases which we don't want ``string``'s characters
        to be confused with.
    :type preferred_aliases: list(str)
    :return: False if not confusable, all confusable characters and with what they are confusable
        otherwise.
    :rtype: bool or list
    """
    preferred_aliases = list(map(str.upper, preferred_aliases))
    outputs = []
    checked = set()
    for char in string:
        if char in checked:
            continue
        checked.add(char)
        char_alias = alias(char)
        if char_alias in preferred_aliases:
            # these are safe: the character is confusable with homoglyphs from other
            # categories than our preferred categories (=aliases)
            continue
        found = confusables_data.get(char)
        if found:  # we found homoglyphs
            output = {
                'character': char,
                'alias': char_alias,
                'homoglyphs': found,
            }
            if not greedy:
                return [output]
            outputs.append(output)

    return outputs or False


def is_dangerous(string, preferred_aliases=[]):
    """Checks if ``string`` can be dangerous, i.e. is it not only mixed-scripts
    but also contains characters from other scripts than the ones in ``preferred_aliases``
    that might be confusable with characters from scripts in ``preferred_aliases``

    For ``preferred_aliases`` examples, see ``is_confusable`` docstring.

    :param string: A unicode string
    :type string: str
    :param preferred_aliases: Script blocks aliases which we don't want ``string``'s characters
        to be confused with.
    :type preferred_aliases: list(str)
    :return: Is it dangerous.
    :rtype: bool
    """
    return is_mixed_script(string) and is_confusable(string, *preferred_aliases)


def generate():
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

    confusables_matrix = dict(confusables_matrix)

    with open('{}/confusables.json'.format(os.getcwd()), 'w+') as datafile:
        json.dump(confusables_matrix, datafile)
    return True


try:
    confusables_data = load('confusables.json')
except:
    try:
        if generate():
            confusables_data = load('confusables.json')
    except:
        raise Exception('Datafile not found, datafile generation failed!')
