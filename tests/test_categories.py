#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from confusable_homoglyphs import categories, utils

latin_a = u'A'
greek_a = u'Α'

is_good = 'Allo'
looks_good = is_good.replace(latin_a, greek_a)


class TestCategories(unittest.TestCase):
    def test_generating(self):
        utils.delete('categories.json')
        self.assertTrue(categories.generate())

    def test_aliases_categories(self):
        self.assertEqual(categories.aliases_categories(latin_a), (
            categories.alias(latin_a), categories.category(latin_a)))
        self.assertEqual(categories.aliases_categories(greek_a), (
            categories.alias(greek_a), categories.category(greek_a)))

    def test_alias(self):
        self.assertEqual(categories.alias(latin_a), 'LATIN')
        self.assertEqual(categories.alias(greek_a), 'GREEK')

    def test_category(self):
        self.assertEqual(categories.category(latin_a), 'L')
        self.assertEqual(categories.category(greek_a), 'L')

    def test_unique_aliases(self):
        self.assertEqual(categories.unique_aliases(is_good), set(['LATIN']))
        self.assertEqual(categories.unique_aliases(looks_good), set(['GREEK', 'LATIN']))


if __name__ == '__main__':
    unittest.main()
