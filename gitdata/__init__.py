#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import os
import subprocess

from git import git_root

def gitdata_path():
    return os.path.join(git_root(), '.gitdata')

def sha1sum(content):
    return hashlib.sha1(content).hexdigest()

def file_sha1sum(filepath):
    return sha1sum(open(filepath, 'rb').read())

def get_file_list(d="."):

    file_list = []
    for root, dirs, files in os.walk(d, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))

    return file_list

def gitdata_readlines():
    try:
        return open(gitdata_path()).readlines()
    except IOError:
        return []

def get_gitdata_info():
    info = {}

    for line in gitdata_readlines():
        line = line.replace('\n','').split(" ")
        sha1, file_path = line[:2]
        info[file_path] = {'sha1':sha1}
        if len(line) == 3:
            info[file_path]['remote'] = line[2]

    return info

def remote_sync(cmd='push'):
    gitdata_info = get_gitdata_info()

    for file_path, info in gitdata_info.items():
        if 'remote' in info:
            remote = info['remote']
            sha1 = info['sha1']
            file_name = os.path.basename(file_path)
            remote = "{}{}_{}".format(remote, sha1, file_name)

            if cmd == 'push':
                scp = "scp {} {}".format(file_path, remote)
            else:
                scp = "scp {} {}".format(remote, file_path)

            print scp
            subprocess.check_output(scp.split(" "))

def status():
    """ check sha1 of file with sha1 in .gitdata """
    gitdata_info = get_gitdata_info()
    for file_path in gitdata_info.keys():
        if file_sha1sum(file_path) != gitdata_info[file_path]['sha1']:
            print "modified:\t"+file_path

def list_files():
    gitdata_info = get_gitdata_info()
    for file_path in gitdata_info.keys():
        print file_path

def add(d):
    """ add or update sha1 of files """

    try:
        gitdata_info = get_gitdata_info()
    except IOError:
        gitdata_info = {}

    files = get_file_list(d)
    previous_files = gitdata_info.keys()
    for f in files:
        if f not in previous_files:
            gitdata_info[f] = {}
        gitdata_info[f]['sha1'] = file_sha1sum(f)

    gitdata = open(gitdata_path(), 'w')
    for file_path in sorted(gitdata_info.keys()):
        info = gitdata_info[file_path]

        sha1 = info['sha1']
        line = "{} {}".format(sha1, file_path)

        if 'remote' in info:
            line += " {}".format(info['remote'])

        line += '\n'
        gitdata.write(line)

    gitdata.close()

