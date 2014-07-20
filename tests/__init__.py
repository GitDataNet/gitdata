#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from gitdata import sha1sum
from gitdata import gitdata_info
from gitdata import make_gitdata_content
from gitdata import make_ssh_cmd
from gitdata import update_gitdata_info
from gitdata import make_status_lines
from gitdata import remote_split

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
            '96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt server\n'
        ]
        info = {
            "data/data2.txt": {
                "sha1": "96e93e946f7fd810b167e34561c489ce067d7ef1",
                "remote": "server",
            }
        }

        self.assertEqual(gitdata_info(content), info)

    def test_gitdata_info_one_line_remote_with_port(self):

        content = [
            '96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt s:path:8080\n'
        ]

        info = gitdata_info(content)

        self.assertEqual(info["data/data2.txt"]['port'], '8080')

    def test_gitdata_info_one_line_remote_without_port(self):

        content = [
            '96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt s:path\n'
        ]

        info = gitdata_info(content)

        self.assertTrue('port' not in info["data/data2.txt"].keys())

    def test_remote_split_with_port(self):
        remote_str= 'user@serve:path:8080'

        self.assertEqual(remote_split(remote_str), ('user@serve:path','8080'))

    def test_remote_split_without_port(self):
        remote_str= 'user@serve:path'

        remote = remote_split(remote_str)

        self.assertEqual(remote, remote_str)

    def test_make_gitdata_content(self):
        gitdata_info = {
            "data/data2.txt": {
                "sha1": "96e93e946f7fd810b167e34561c489ce067d7ef1",
                "remote": "server",
            }
        }

        content = '96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt server\n'

        self.assertEqual(make_gitdata_content(gitdata_info), content)

    def test_update_gitdata_info_one_file(self):
        gitdata_info = {
            "data/data2.txt": {
                "sha1": "0000000000000000000000000000000000000000",
            }
        }

        new_files_sha1 = {
            "data/data2.txt": "1111111111111111111111111111111111111111",
        }

        updated= {
            "data/data2.txt": {
                "sha1": "1111111111111111111111111111111111111111",
            }
        }

        self.assertEqual(updated,\
                update_gitdata_info(gitdata_info, new_files_sha1))

    def test_update_gitdata_info_one_new_file(self):
        gitdata_info = {}

        new_files_sha1 = {
            "data/data2.txt": "1111111111111111111111111111111111111111",
        }

        updated= {
            "data/data2.txt": {
                "sha1": "1111111111111111111111111111111111111111",
            }
        }

        self.assertEqual(updated,\
                update_gitdata_info(gitdata_info, new_files_sha1))

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

    def test_make_status_lines_sha1_none(self):
        gitdata_info = {
            "data/data2.txt": {
                "sha1": "0000000000000000000000000000000000000000",
            }
        }

        files_sha1 = {
            "data/data2.txt": None,
        }

        content = 'deleted:\tdata/data2.txt\n'

        self.assertEqual(content,\
            make_status_lines(gitdata_info, files_sha1))


class TestSsh(unittest.TestCase):

    def setUp(self):
        self.gitdata_info = {
            "data/data2.txt": {
                "sha1": "96e93e946f7fd810b167e34561c489ce067d7ef1",
                "remote": "server",
            },
            "data/data1.txt": {
                "sha1": "c859bff85da4add4298835c9551d6d9ac3afdeca",
            }
        }
        self.gitdata_info_port = {
            "data/data2.txt": {
                "sha1": "96e93e946f7fd810b167e34561c489ce067d7ef1",
                "remote": "u@s:tmp/",
                "port": "8080",
            },
        }

    def test_make_ssh_cmd_push(self):
        gitdata_info = self.gitdata_info
        cmd = 'push'

        ssh_cmd_lines = [
            'scp data/data2.txt server96e93e946f7fd810b167e34561c489ce067d7ef1_data2.txt',
        ]

        self.assertEqual(make_ssh_cmd(gitdata_info, cmd), ssh_cmd_lines)

    def test_make_ssh_cmd_pull(self):
        gitdata_info = self.gitdata_info
        cmd = 'pull'

        ssh_cmd_lines = [
            'scp server96e93e946f7fd810b167e34561c489ce067d7ef1_data2.txt data/data2.txt'
        ]

        self.assertEqual(make_ssh_cmd(gitdata_info, cmd), ssh_cmd_lines)

    def test_make_ssh_cmd_push_with_port(self):
        gitdata_info = self.gitdata_info_port
        cmd = 'push'

        ssh_cmd_lines = [
            'scp -P 8080 data/data2.txt u@s:tmp/96e93e946f7fd810b167e34561c489ce067d7ef1_data2.txt',
        ]

        self.assertEqual(make_ssh_cmd(gitdata_info, cmd), ssh_cmd_lines)

    def test_make_ssh_cmd_pull_with_port(self):
        gitdata_info = self.gitdata_info_port
        cmd = 'pull'

        ssh_cmd_lines = [
                'scp -P 8080 u@s:tmp/96e93e946f7fd810b167e34561c489ce067d7ef1_data2.txt data/data2.txt'
        ]

        self.assertEqual(make_ssh_cmd(gitdata_info, cmd), ssh_cmd_lines)

