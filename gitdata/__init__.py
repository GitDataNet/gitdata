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
        info[sha1] = file_path

    return info

def status():
    """ check sha1 of file with sha1 in .gitdata """
    for sha1, file_path in  get_gitdata_info().items():
        if sha1 != file_sha1sum(file_path):
            print file_path

def commit():
    """ write .gitdata file """
    pass

def add(d):
    gitdata = open(gitdata_path(), 'w')

    files = get_file_list(d)
    for f in files:
        line = "{} {}\n".format(file_sha1sum(f), f)
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
