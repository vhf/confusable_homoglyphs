# -*- coding: utf-8 -*-
import json
import os
import sys

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))

if sys.version_info < (3,):
    import codecs
    from urllib2 import urlopen

    def u(x):
        return codecs.unicode_escape_decode(x)[0]

    def get(url, timeout=None):
        return urlopen(url, timeout=timeout)

else:
    from urllib.request import urlopen

    def u(x):
        return x

    def get(url, timeout=None):
        return urlopen(url, timeout=timeout).read().decode('utf-8').split('\n')


def path(filename):
    """Returns a file path relative to this package directory.

    :return: A file path string.
    :rtype: str
    """
    return os.path.join(PACKAGE_DIR, filename)


def load(filename):
    """Loads a JSON data file.

    :return: A dict.
    :rtype: dict
    """
    with open(path(filename), 'r') as file:
        return json.load(file)


def dump(filename, data):
    with open(path(filename), 'w+') as file:
        return json.dump(data, file)


def delete(filename):
    """Deletes a JSON data file if it exists.
    """
    try:
        os.remove(path(filename))
    except OSError:
        pass
