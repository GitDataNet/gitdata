#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

setup(
    name = "git-data",
    version = "0.0.1",
    author = "JuanPablo AJ",
    author_email = "jpabloaj@gmail.com",
    test_suite = "tests",
    scripts=['bin/git-data'],
    classifiers = [
        'Programming Language :: Python :: 2.7',
    ]
)
