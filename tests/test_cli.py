
from os.path import isfile
import unittest

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError

from confusable_homoglyphs.cli import generate_categories, generate_confusables
from confusable_homoglyphs.utils import get, delete


def unicode_org_down():
    try:
        get('https://www.unicode.org', timeout=5)
        return False
    except URLError:
        return True


@unittest.skipIf(unicode_org_down(), 'www.unicode.org is down')
class TestUpdate(unittest.TestCase):
    def test_generate_categories(self):
        delete('categories.json')
        self.assertFalse(isfile('categories.json'))

        generate_categories()
        self.assertTrue(isfile('categories.json'))

    def test_generate_confusables(self):
        delete('confusables.json')
        self.assertFalse(isfile('confusables.json'))

        generate_confusables()
        self.assertTrue(isfile('confusables.json'))
