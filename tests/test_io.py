#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import tempfile
import os

from gitdata import get_file_list
from gitdata import file_sha1sum
from gitdata import files_sha1sum


class TestIO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
        cls.dir_name = 'files'
        cls.files_dir = os.path.join(cls.tempdir, cls.dir_name)
        os.mkdir(cls.files_dir)

        new_files = ['file1.txt', 'file2.txt']

        for fname in new_files:
            open(os.path.join(cls.files_dir, fname), 'w').write(fname)

    def test_list_files(self):
        os.chdir(self.tempdir)

        paths = ['files/file1.txt', 'files/file2.txt']

        self.assertItemsEqual(get_file_list(self.dir_name), paths)

    def test_file_sha1sum(self):

        file_path = os.path.join(self.files_dir, 'file1.txt')

        self.assertEqual(
            file_sha1sum(file_path),
            'ce1be0ff4065a6e9415095c95f25f47a633cef2b'
        )

    def test_file_sha1sum_file_not_found(self):

        file_path = os.path.join(self.files_dir, 'fail_file.txt')

        self.assertEqual(file_sha1sum(file_path), None)

    def test_files_sha1sum(self):

        path_list = get_file_list(self.files_dir)
        expected = {
            os.path.join(self.files_dir, 'file1.txt'):
            'ce1be0ff4065a6e9415095c95f25f47a633cef2b',
            os.path.join(self.files_dir, 'file2.txt'):
            'c2edf7b002d0354039a8aaba3bc53180caf3d248',
        }

        self.assertEqual(files_sha1sum(path_list), expected)
