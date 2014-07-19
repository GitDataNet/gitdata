#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import os
import argparse
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
    return open(gitdata_path()).readlines()

def get_gitdata_info():
    info = {}

    for line in gitdata_readlines():
        sha1, file_path = line.replace('\n','').split(" ")
        info[file_path] = sha1

    return info

def status():
    """ check sha1 of file with sha1 in .gitdata """
    for file_path, sha1 in  get_gitdata_info().items():
        if file_sha1sum(file_path) != sha1:
            print "modified:\t"+file_path

def add(d):
    """ add or update sha1 of files """

    try:
        gitdata_info = get_gitdata_info()
    except IOError:
        gitdata_info = {}

    files = get_file_list(d)
    for f in files:
        gitdata_info[f] = file_sha1sum(f)

    gitdata = open(gitdata_path(), 'w')
    for file_path in sorted(gitdata_info.keys()):
        sha1 = gitdata_info[file_path]
        line = "{} {}\n".format(sha1, file_path)
        gitdata.write(line)

    gitdata.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--add', default=None)
    parser.add_argument('status', nargs='?')
    args = parser.parse_args()

    if args.status:
        status()
    elif args.add:
        add(args.add)

if __name__ == '__main__':
    main()
