#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name = "gitdata",
    version = "0.0.1",
    description = "Storage the data files in ssh servers",
    long_description=(read('README.rst')),
    url = "https://github.com/juanpabloaj/gitdata",
    license='MIT',
    author = "JuanPablo AJ",
    author_email = "jpabloaj@gmail.com",
    packages = ['bin', 'gitdata'],
    test_suite = "tests",
    entry_points={
        'console_scripts': [
            'git-data=bin:main',
        ],
    },
    classifiers = [
        'Programming Language :: Python :: 2.7',
    ]
)
