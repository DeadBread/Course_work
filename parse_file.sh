#!/bin/bash
MYPWD=$(pwd)
cd "../syntaxNet/models/syntaxnet"
syntaxnet/models/parsey_universal/parse.sh ~/lib/models/Russian-SynTagRus < "$MYPWD/$1" > $MYPWD/output.txt

