#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess

def git_root():
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])\
            .replace('\n','')
