``ϲοｎｆｕѕаｂｌе＿һοｍоɡｌｙｐｈｓ``
=========================

``confusable_homoglyphs``
=========================

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
-  ``Alloτ`` is fine: mixed script, but ``τ`` is not confusable.
-  ``Alloρ`` is dangerous: mixed script and ``ρ`` could be confused with
   ``p``.

Documentation
-------------

``confusables``
~~~~~~~~~~~~~~~

.. code:: python

    from confusable_homoglyphs import confusables

``confusables.is_mixed_script``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    confusables.is_mixed_script(unicode_string)

Boolean: is the mixed-script.

``confusables.is_confusable``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    confusables.is_confusable(unicode_string, greedy=False, preferred_aliases=[])

Takes a character or string and returns each character present in
unicode's `confusable characters
list <http://www.unicode.org/Public/security/latest/confusables.txt>`__.

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
      latin ``p``.
   -  with ``preferred_aliases=[]`` and ``greedy=True``, you'll discover
      the 29 characters that can be confused with ``p``, the 23
      characters that look like ``a``, and the one that looks like ``ρ``
      (which is, of course, *p* aka *LATIN SMALL LETTER P*).

``confusables.is_dangerous``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    confusables.is_dangerous(unicode_string, preferred_aliases=['latin'])

Boolean: ``True`` if is\_mixed\_script(unicode\_string) *and*
is\_confusable(unicode\_string).

The ``preferred_aliases`` argument is simply passed to
``is_confusable``.

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
