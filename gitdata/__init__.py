#!/usr/bin/python
# -*- coding: utf-8 -*-
""" gitdata """

import hashlib
import os
import sys
import subprocess
import copy

from gitdata.git import git_root


def gitdata_path():
    """ return path of gitdata file """
    return os.path.join(git_root(), '.gitdata')


def sha1sum(content):
    """ return SHA1 sum of content """
    return hashlib.sha1(content).hexdigest()


def file_sha1sum(filepath):
    """ return SHA1 sum of file """
    try:
        return sha1sum(open(filepath, 'rb').read())
    except IOError:
        return


def files_sha1sum(path_list):
    """ return dictionary with SHA1 sum of list of files """
    return dict((f, file_sha1sum(f)) for f in path_list)


def remote_split(remote_str):
    """ split remote url with port """
    splitted = remote_str.split(':')
    if len(splitted) == 3:
        return ':'.join(splitted[:-1]), splitted[-1]

    return remote_str


def get_file_list(dir_name="."):
    """ return list of files in directory """

    file_list = []
    for root, _, files in os.walk(dir_name, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))

    return file_list


def gitdata_readlines():
    """ return gitdata file lines """
    try:
        return open(gitdata_path()).readlines()
    except IOError:
        return []


def gitdata_info(lines):
    """ return dictionary with info of gitdata lines """
    info = {}

    for line in lines:
        line = line.replace('\n', '').split(" ")
        sha1, file_path = line[:2]
        info[file_path] = {'sha1': sha1}
        if len(line) == 3:
            remote_str = remote_split(line[2])
            info[file_path]['remote'] = remote_str
            if len(remote_str) == 2:
                info[file_path]['remote'] = remote_str[0]
                info[file_path]['port'] = remote_str[1]
    return info


def get_gitdata_info():
    """ return gitdata file info """
    return gitdata_info(gitdata_readlines())


def make_ssh_cmd(gitdata_info_dict, cmd):
    """ make ssh command with info in gitdata file """
    ssh_cmd_lines = []

    for file_path, info in gitdata_info_dict.items():
        if 'remote' in info:

            file_name = os.path.basename(file_path)
            remote = "{}{}_{}".format(info['remote'], info['sha1'], file_name)

            port = ''
            if 'port' in info.keys():
                port = '-P {} '.format(info["port"])

            if cmd == 'push':
                scp = "scp {}{} {}".format(port, file_path, remote)
            else:
                scp = "scp {}{} {}".format(port, remote, file_path)

            ssh_cmd_lines.append(scp)

    return ssh_cmd_lines


def remote_sync(cmd='push'):
    """ call ssh command """
    if status() != '' and cmd == 'push':
        return

    for scp in make_ssh_cmd(get_gitdata_info(), cmd):
        print scp
        subprocess.check_output(scp.split(" "))


def make_status_lines(gitdata_info_dict, files_sha1):
    """ print names of modified or deleted files """
    lines = ''

    for file_path in gitdata_info_dict.keys():
        file_path_sha1 = files_sha1[file_path]
        if not file_path_sha1:
            lines += "deleted:\t{}\n".format(file_path)
        elif file_path_sha1 != gitdata_info_dict[file_path]['sha1']:
            lines += "modified:\t{}\n".format(file_path)

    return lines


def status():
    """ check sha1 of file with sha1 in .gitdata """
    gitdata_info_dict = get_gitdata_info()
    files_sha1 = files_sha1sum(gitdata_info_dict.keys())

    status_lines = make_status_lines(gitdata_info_dict, files_sha1)
    sys.stdout.write(status_lines)

    return status_lines


def list_files():
    """ print files listed in gitdata """
    gitdata_info_dict = get_gitdata_info()
    for file_path in gitdata_info_dict.keys():
        print file_path


def make_gitdata_content(gitdata_info_dict):
    """ create gitdata content from info dictionary """
    content = ''

    for file_path in sorted(gitdata_info_dict.keys()):
        info = gitdata_info_dict[file_path]

        sha1 = info['sha1']
        line = "{} {}".format(sha1, file_path)

        if 'remote' in info:
            line += " {}".format(info['remote'])

        line += '\n'
        content += line

    return content


def update_gitdata_info(gitdata_info_dict, new_files_sha1):
    """ update info of gitdata dictionary """
    previous_files = gitdata_info_dict.keys()
    updated = copy.deepcopy(gitdata_info_dict)

    for file_name in new_files_sha1.keys():
        if file_name not in previous_files:
            updated[file_name] = {}
        updated[file_name]['sha1'] = new_files_sha1[file_name]

    return updated


def add(dir_name):
    """ add or update sha1 of files """

    new_files_sha1 = files_sha1sum(get_file_list(dir_name))

    gitdata_info_dict = update_gitdata_info(get_gitdata_info(), new_files_sha1)

    gitdata = open(gitdata_path(), 'w')
    gitdata.write(make_gitdata_content(gitdata_info_dict))
    gitdata.close()
