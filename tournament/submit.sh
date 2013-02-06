#!/bin/bash
#Be sure to chmod u+x this file!

#Your team name (Please keep this the same, and make sure it is a legal filename... no spaces/symbols/etc)
TEAM='default'

if [ $# -ne 1 ]; then
   echo 1>&2 Usage: $0 filename
   exit 127
fi

python fileclient.py rc05cslinux.managed.mst.edu 18000 $1 $TEAM

echo 'File submitted'
