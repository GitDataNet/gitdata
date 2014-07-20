#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gitdata import sha1sum
from gitdata import gitdata_info
from gitdata import make_gitdata_content
from gitdata import make_ssh_cmd
from gitdata import update_gitdata_info
from gitdata import make_status_lines

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

    def test_gitdata_info_one_line_with_remote(self):

        content = [
            '96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt ssh:server\n'
        ]
        info = {
            "data/data2.txt": {
                "sha1": "96e93e946f7fd810b167e34561c489ce067d7ef1",
                "remote": "ssh:server",
            }
        }

        self.assertEqual(gitdata_info(content), info)

    def test_make_gitdata_content(self):
        gitdata_info = {
            "data/data2.txt": {
                "sha1": "96e93e946f7fd810b167e34561c489ce067d7ef1",
                "remote": "ssh:server",
            }
        }

        content = '96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt ssh:server\n'

        self.assertEqual(make_gitdata_content(gitdata_info), content)

    def test_update_gitdata_info_one_file(self):
        gitdata_info = {
            "data/data2.txt": {
                "sha1": "0000000000000000000000000000000000000000",
            }
        }

        previous_files = ["data/data2.txt"]
        new_files_sha1 = {
            "data/data2.txt": "1111111111111111111111111111111111111111",
        }

        updated= {
            "data/data2.txt": {
                "sha1": "1111111111111111111111111111111111111111",
            }
        }

        self.assertEqual(updated,\
                update_gitdata_info(gitdata_info, previous_files, new_files_sha1))

    def test_update_gitdata_info_one_new_file(self):
        gitdata_info = {}

        previous_files = []
        new_files_sha1 = {
            "data/data2.txt": "1111111111111111111111111111111111111111",
        }

        updated= {
            "data/data2.txt": {
                "sha1": "1111111111111111111111111111111111111111",
            }
        }

        self.assertEqual(updated,\
                update_gitdata_info(gitdata_info, previous_files, new_files_sha1))

    def test_make_status_lines(self):
        gitdata_info = {
            "data/data2.txt": {
                "sha1": "0000000000000000000000000000000000000000",
            }
        }

        files_sha1 = {
            "data/data2.txt": "1111111111111111111111111111111111111111",
        }

        content = 'modified:\tdata/data2.txt\n'

        self.assertEqual(content,\
            make_status_lines(gitdata_info, files_sha1))

class TestSsh(unittest.TestCase):

    def setUp(self):
        self.gitdata_info = {
            "data/data2.txt": {
                "sha1": "96e93e946f7fd810b167e34561c489ce067d7ef1",
                "remote": "ssh:server",
            },
            "data/data1.txt": {
                "sha1": "c859bff85da4add4298835c9551d6d9ac3afdeca",
            }
        }

    def test_make_ssh_cmd_push(self):
        gitdata_info = self.gitdata_info
        cmd = 'push'

        ssh_cmd_lines = [
            'scp data/data2.txt ssh:server96e93e946f7fd810b167e34561c489ce067d7ef1_data2.txt',
        ]

        self.assertEqual(make_ssh_cmd(gitdata_info, cmd), ssh_cmd_lines)

    def test_make_ssh_cmd_pull(self):
        gitdata_info = self.gitdata_info
        cmd = 'pull'

        ssh_cmd_lines = [
            'scp ssh:server96e93e946f7fd810b167e34561c489ce067d7ef1_data2.txt data/data2.txt'
        ]

        self.assertEqual(make_ssh_cmd(gitdata_info, cmd), ssh_cmd_lines)
