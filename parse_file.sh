#!/bin/bash
MYPWD=$(pwd)
cd "syntaxNet/models/syntaxnet"
syntaxnet/models/parsey_universal/parse.sh /home/gand/lib/models/Russian-SynTagRus < "$1"  > "$MYPWD/output.txt"

