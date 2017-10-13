
from os.path import isfile
import unittest

from confusable_homoglyphs.cli import generate_categories, generate_confusables
from confusable_homoglyphs.utils import delete


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
