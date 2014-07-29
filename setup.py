#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gitdata setup.py """

import os
from setuptools import setup


def read(*paths):
    """ read files """
    with open(os.path.join(*paths), 'r') as filename:
        return filename.read()

setup(
    name="gitdata",
    version="0.0.2",
    description="Storage the data files in ssh servers",
    long_description=(read('README.rst')),
    url="https://github.com/juanpabloaj/gitdata",
    license='MIT',
    author="JuanPablo AJ",
    author_email="jpabloaj@gmail.com",
    packages=['bin', 'gitdata'],
    test_suite="tests",
    entry_points={
        'console_scripts': [
            'git-data=bin:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ]
)
