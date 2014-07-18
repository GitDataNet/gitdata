#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

def sha1sum(content):
    return hashlib.sha1(content).hexdigest()

def main():
    pass

if __name__ == '__main__':
    main()
