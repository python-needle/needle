#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='needle',
    version='0.0.2',
    description='Automated testing for your CSS.',
    author='Ben Firshman',
    author_email='ben@firshman.co.uk',
    url='https://github.com/bfirsh/needle',
    packages=find_packages(exclude=['scripts', 'tests']),
    package_data={'needle': ['js/*']},
    test_suite='nose.collector',
    entry_points = {
        'nose.plugins.0.10': [
            'needle-capture = needle.plugin:NeedleCapturePlugin'
        ]
    },
    install_requires=[
        'nose>=1.0.0',
        'selenium>=2,<3',
        'unittest2>=0.5.1',
        'pillow',
    ],
)

