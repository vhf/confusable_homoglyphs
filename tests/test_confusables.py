#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from confusable_homoglyphs import confusables, utils

latin_a = u'A'
greek_a = u'Α'

is_good = 'Allo'
looks_good = is_good.replace(latin_a, greek_a)


class TestConfusables(unittest.TestCase):
    def test_generating(self):
        utils.delete('confusables.json')
        self.assertTrue(confusables.generate())

    def test_is_mixed_script(self):
        self.assertTrue(confusables.is_mixed_script(looks_good))
        self.assertTrue(confusables.is_mixed_script(u' ρττ a'))

        self.assertFalse(confusables.is_mixed_script(is_good))
        self.assertFalse(confusables.is_mixed_script(u'ρτ.τ'))
        self.assertFalse(confusables.is_mixed_script(u'ρτ.τ '))

        try:
            confusables.is_mixed_script('', allowed_aliases=[u'COMMON'])
        except TypeError:
            self.fail('TypeError when allowed_aliases provided as unicode')

    def test_is_confusable(self):
        greek = confusables.is_confusable(looks_good, preferred_aliases=['latin'])
        self.assertEqual(greek[0]['character'], greek_a)
        self.assertIn({'c': 'A', 'n': 'LATIN CAPITAL LETTER A'}, greek[0]['homoglyphs'])
        latin = confusables.is_confusable(is_good, preferred_aliases=['latin'])
        self.assertFalse(latin)

        self.assertFalse(confusables.is_confusable(u'AlloΓ', preferred_aliases=['latin']))

        # stop at first confusable character
        self.assertEqual(len(confusables.is_confusable(u'Αlloρ', greedy=False)), 1)
        # find all confusable characters
        # Α (greek), l, o, and ρ can be confused with other unicode characters
        self.assertEqual(len(confusables.is_confusable(u'Αlloρ', greedy=True)), 4)
        # Only Α (greek) and ρ (greek) can be confused with a latin character
        self.assertEqual(
            len(confusables.is_confusable(u'Αlloρ', greedy=True, preferred_aliases=['latin'])), 2)

        # for 'Latin' readers, ρ is confusable!    ↓
        confusable = confusables.is_confusable(u'paρa', preferred_aliases=['latin'])[0]['character']
        self.assertEqual(confusable, u'ρ')
        # for 'Greek' readers, p is confusable!  ↓
        confusable = confusables.is_confusable(u'paρa', preferred_aliases=['greek'])[0]['character']
        self.assertEqual(confusable, 'p')

        try:
            confusables.is_confusable('', preferred_aliases=[u'latin'])
        except TypeError:
            self.fail('TypeError when preferred_aliases provided as unicode')

    def test_dangerous(self):
        self.assertTrue(confusables.is_dangerous(looks_good))
        self.assertTrue(confusables.is_dangerous(u' ρττ a'))
        self.assertTrue(confusables.is_dangerous(u'ρττ a'))
        self.assertTrue(confusables.is_dangerous(u'Alloτ'))
        self.assertTrue(confusables.is_dangerous(u'www.micros﻿оft.com'))
        self.assertTrue(confusables.is_dangerous(u'www.Αpple.com'))
        self.assertTrue(confusables.is_dangerous(u'www.faϲebook.com'))
        self.assertFalse(confusables.is_dangerous(u'AlloΓ', preferred_aliases=['latin']))
        self.assertFalse(confusables.is_dangerous(is_good))
        self.assertFalse(confusables.is_dangerous(u' ρτ.τ'))
        self.assertFalse(confusables.is_dangerous(u'ρτ.τ'))


if __name__ == '__main__':
    unittest.main()
