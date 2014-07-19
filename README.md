# git data

## .gitdata file

    SHA1 path remote_ssh

Example

    c00214008bcd3fe1f5beccdf1a63d15b158bf0b3 data/data1.txt ssh://server:tmp/
    96e93e946f7fd810b167e34561c489ce067d7ef1 data/data2.txt

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
