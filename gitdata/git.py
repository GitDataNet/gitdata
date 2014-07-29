#!/usr/bin/python
# -*- coding: utf-8 -*-
""" git functions """

import subprocess


def git_root():
    """ return git root directory """
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])\
        .replace('\n', '')
