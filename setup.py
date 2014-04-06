#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
import os
import codecs

from needle import __version__

# Borrowed from
# https://github.com/jezdez/django_compressor/blob/develop/setup.py
def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts)).read()


install_requires = [
    'nose>=1.0.0',
    'selenium>=2,<3',
    'pillow',
]

if sys.version_info < (2, 7, 0):
    # Install backport of unittest2 only if needed.
    install_requires.append('unittest2>=0.5.1')


setup(
    name='needle',
    version=__version__,
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
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Multimedia :: Graphics :: Capture :: Screen Capture',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)

