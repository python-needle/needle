#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re
import os
import codecs


# Borrowed from
# https://github.com/jezdez/django_compressor/blob/develop/setup.py
def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='needle',
    version=find_version("needle", "__init__.py"),
    description='Automated testing for your CSS.',
    author='Ben Firshman',
    author_email='ben@firshman.co.uk',
    url='https://github.com/bfirsh/needle',
    packages=find_packages(exclude=['scripts', 'tests']),
    package_data={'needle': ['js/*']},
    test_suite='nose.collector',
    entry_points = {
        'nose.plugins.0.10': [
            'needle-capture = needle.plugin:NeedleCapturePlugin',
            'save-baseline = needle.plugin:SaveBaselinePlugin'
        ]
    },
    install_requires=[
        'nose>=1.0.0',
        'selenium>=2,<3',
        'unittest2>=0.5.1',
        'pillow',
    ],
)

