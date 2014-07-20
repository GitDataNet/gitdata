# git data

[![Coverage Status](https://coveralls.io/repos/juanpabloaj/gitdata/badge.png?branch=master)](https://coveralls.io/r/juanpabloaj/gitdata?branch=master)

Storage the data files (images, data test) in remote ssh servers. In git only save a register of necessary files to current commit.

## .gitdata file

    SHA1 path remote_ssh:ssh_port

Example

    96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt
    c00214008bcd3fe1f5beccdf1a63d15b158bf0b3 data/data1.txt user@server:tmp/
    7a7a91f5c2b5bc1f4d294de5a6166abec5364d15 data/data0.txt user@server:tmp/:1234

## Usage

Add to `.gitdata` file, [SHA-1](http://en.wikipedia.org/wiki/SHA-1) and path of files contained in the directory.

    git data -a directory

Show modified files, files with modified `SHA-1`

    git data status

Files with ssh column are pushed to remote ssh server

    git data -p

Files with ssh column are pulled from remote ssh server, the version download is respective to the current SHA-1 in `.gitdata` file.

    git data -u

Show files stored in the `.gitdata` file

    git data -l
