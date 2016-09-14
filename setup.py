#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import versioneer
from codecs import open
from os import path
from setuptools import setup, find_packages


def test_suite():
    test_loader = unittest.TestLoader()
    suite = test_loader.discover('tests', pattern='test_*.py')
    return suite


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
]

test_requirements = [
]

setup(
    name='confusable_homoglyphs',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Detect confusable usage of unicode homoglyphs, prevent homograph attacks.',
    long_description=readme + '\n\n' + history,
    author='Victor Felder',
    author_email='victorfelder@gmail.com',
    url='https://github.com/vhf/confusable_homoglyphs',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'confusable_homoglyphs=confusable_homoglyphs.cli:cli',
            ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    keywords=['confusable', 'homoglyph', 'attack', 'homograph', 'unicode', 'spoofing'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    test_suite='setup.test_suite',
    tests_require=test_requirements
)
