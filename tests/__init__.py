#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from lib.gitdata import sha1sum

class TestSha1(unittest.TestCase):

    def test_sha1sum(self):

        self.assertEqual(sha1sum('test'), 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3')
