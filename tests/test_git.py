#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import tempfile
import os
import subprocess

from gitdata.git import git_root
from gitdata import gitdata_path

class TestGit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()

    def setUp(self):
        os.chdir(self.tempdir)

    def test_git_root(self):
        subprocess.check_output(['git', 'init'])

        self.assertEqual(self.tempdir, git_root())

    def test_gitdata_path(self):
        path = '{}/{}'.format(self.tempdir, '.gitdata')

        self.assertEqual(gitdata_path(), path)

