#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import os
import argparse

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

def status():
    """ check sha1 file with .gitdata file """
    pass

def commit():
    """ write .gitdata file """
    pass

def add(d):
    files = get_file_list(d)
    for f in files:
        print file_sha1sum(f), f

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--add', default=None)
    args = parser.parse_args()

    if args.add:
        add(args.add)

if __name__ == '__main__':
    main()
