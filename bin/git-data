#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from gitdata import status, add, remote_sync, list_files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--add', default=None)
    parser.add_argument('-p','--push', action='store_true')
    parser.add_argument('-u','--pull', action='store_true')
    parser.add_argument('-l','--list', action='store_true')
    parser.add_argument('status', nargs='?')
    args = parser.parse_args()

    if args.status:
        status()
    elif args.add:
        add(args.add)
    elif args.push:
        remote_sync('push')
    elif args.pull:
        remote_sync('pull')
    elif args.list:
        list_files()

if __name__ == '__main__':
    main()
