#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gitdata import sha1sum
from gitdata import gitdata_info

class TestSha1(unittest.TestCase):

    def test_sha1sum(self):

        self.assertEqual(sha1sum('test'), 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3')

class TestGitdata(unittest.TestCase):

    def test_gitdata_info_one_line(self):

        content = ['96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt\n']
        info = {
            "data/data2.txt":
                {"sha1": "96e93e946f7fd810b167e34561c489ce067d7ef1"}
        }

        self.assertEqual(gitdata_info(content), info)
