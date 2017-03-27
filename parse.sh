#!/bin/bash
MYPWD=$(pwd)
cd "../syntaxNet/models/syntaxnet"
echo " $1 " |   syntaxnet/models/parsey_universal/parse.sh ~/lib/models/Russian-SynTagRus > $MYPWD/output.txt
