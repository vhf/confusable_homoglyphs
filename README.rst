confusable_homoglyphs `[doc] <http://confusable-homoglyphs.readthedocs.io/en/latest/>`__
========================================================================================

.. image:: https://img.shields.io/travis/vhf/confusable_homoglyphs.svg
        :target: https://travis-ci.org/vhf/confusable_homoglyphs

.. image:: https://img.shields.io/pypi/v/confusable_homoglyphs.svg
        :target: https://pypi.python.org/pypi/confusable_homoglyphs

.. image:: https://readthedocs.org/projects/confusable_homoglyphs/badge/?version=latest
        :target: http://confusable-homoglyphs.readthedocs.io/en/latest/
        :alt: Documentation Status

*a homoglyph is one of two or more graphemes, characters, or glyphs with
shapes that appear identical or very similar*
`wikipedia:Homoglyph <https://en.wikipedia.org/wiki/Homoglyph>`__

Unicode homoglyphs can be a nuisance on the web. Your most popular
client, AlaskaJazz, might be upset to be impersonated by a trickster who
deliberately chose the username ΑlaskaJazz.

-  ``AlaskaJazz`` is single script: only Latin characters.
-  ``ΑlaskaJazz`` is mixed-script: the first character is a greek
   letter.

You might also want to avoid people being tricked into entering their
password on ``www.micros﻿оft.com`` or ``www.faϲebook.com`` instead of
``www.microsoft.com`` or ``www.facebook.com``. `Here is a
utility <http://unicode.org/cldr/utility/confusables.jsp>`__ to play
with these **confusable homoglyphs**.

Not all mixed-script strings have to be ruled out though, you could only
exclude mixed-script strings containing characters that might be
confused with a character from some unicode blocks of your choosing.

-  ``Allo`` and ``ρττ`` are fine: single script.
-  ``AlloΓ`` is fine when our preferred script alias is 'latin': mixed script, but ``Γ`` is not confusable.
-  ``Alloρ`` is dangerous: mixed script and ``ρ`` could be confused with
   ``p``.

This library is compatible Python 2 and Python 3.

`API documentation <http://confusable-homoglyphs.readthedocs.io/en/latest/apidocumentation.html>`__
---------------------------------------------------------------------------------------------------

Is the data up to date?
-----------------------

Yep.

The unicode blocks aliases and names for each character are extracted
from `this file <http://www.unicode.org/Public/UNIDATA/Scripts.txt>`__
provided by the unicode consortium.

The matrix of which character can be confused with which other
characters is built using `this
file <http://www.unicode.org/Public/security/latest/confusables.txt>`__
provided by the unicode consortium.

This data is stored in two JSON files: ``categories.json`` and
``confusables.json``. If you delete them, they will both be recreated by
downloading and parsing the two abovementioned files and stored as JSON
files again.
