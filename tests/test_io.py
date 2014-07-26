#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import tempfile
import os

from gitdata import get_file_list

class TestIO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()

    def test_list_files(self):
        dir_name = 'files'
        files_dir = os.path.join(self.tempdir, dir_name)
        os.mkdir(files_dir)
        os.chdir(self.tempdir)

        new_files = ['file1.txt', 'file2.txt']

        for fname in new_files:
            open(os.path.join(files_dir, fname), 'w')

        paths = ['files/file1.txt', 'files/file2.txt']

        self.assertEqual(sorted(get_file_list(dir_name)), sorted(paths))
