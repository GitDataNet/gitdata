#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import tempfile
import os
import subprocess

from gitdata.git import git_root
from gitdata import gitdata_path
from gitdata import gitdata_readlines


class TestGit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
        os.chdir(cls.tempdir)
        subprocess.check_output(['git', 'init'])

    def setUp(self):
        os.chdir(self.tempdir)

    def test_git_root(self):

        self.assertEqual(self.tempdir, git_root())

    def test_gitdata_path(self):
        path = '{}/{}'.format(self.tempdir, '.gitdata')

        self.assertEqual(gitdata_path(), path)

    def test_gitdata_readlines_no_file(self):

        self.assertEqual(gitdata_readlines(), [])


class TestGitdata(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
        os.chdir(cls.tempdir)
        subprocess.check_output(['git', 'init'])

    def setUp(self):
        os.chdir(self.tempdir)

    def tearDown(self):
        os.remove('.gitdata')

    def test_gitdata_readlines(self):

        open('.gitdata', 'w').write('aaa\nbbb')
        content = ['aaa\n', 'bbb']

        self.assertEqual(gitdata_readlines(), content)
