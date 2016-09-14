# -*- coding: utf-8 -*-
import json
import os
import sys


if sys.version_info < (3,):
    import codecs
    from urllib2 import urlopen

    def u(x):
        return codecs.unicode_escape_decode(x)[0]

    def get(url):
        return urlopen(url)

else:
    from urllib.request import urlopen

    def u(x):
        return x

    def get(url):
        return urlopen(url).read().decode('utf-8').split('\n')


def load(filename):
    """Loads a JSON data file.

    :return: A dict.
    :rtype: dict
    """
    with open('{}/{}'.format(os.getcwd(), filename), 'r') as file:
        return json.load(file)


def delete(filename):
    """Deletes a JSON data file if it exists.
    """
    try:
        os.remove('{}/{}'.format(os.getcwd(), filename))
    except OSError:
        pass
