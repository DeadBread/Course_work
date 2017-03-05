#!/bin/bash
MYPWD=$(pwd)
cd "syntaxNet/models/syntaxnet"
echo " $1 " |  syntaxnet/models/parsey_universal/parse.sh /home/gand/lib/models/Russian-SynTagRus > "$MYPDW/output.txt"

