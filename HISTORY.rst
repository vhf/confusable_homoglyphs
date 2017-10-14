.. :changelog:

History
-------

1.0.0
=====

Initial release.

2.0.0
=====

- `allowed_categories` renamed to `allowed_aliases`

2.0.1
=====

- Fix a TypeError: https://github.com/vhf/confusable_homoglyphs/pull/2

3.0.0
=====

Courtesy of Ryan P Kilby, via https://github.com/vhf/confusable_homoglyphs/pull/6 :

- Changed file paths to be relative to the `confusable_homoglyphs` package directory instead of the user's current working directory.
- Data files are now distributed with the packaging.
- Fixes tests so that they use the installed distribution instead of the local files. (Originally, the data files were erroneously showing up during testing, despite not being included in the distribution).
- Moves the data file generation into a simple CLI. This way, users have a method for controlling when the data files are updated.
- Since the data files are now included in the distribution, the CLI is made optional. Its dependencies can be installed with the `cli` bundle, eg. `pip install confusable_homoglyphs[cli]`.

