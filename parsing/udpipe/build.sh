#!/bin/bash
# read from args or input, split and retrieve train dict
# sample call:
# ./build.sh heliand.conllu

if [ ! -e split ]; then
	mkdir split
fi;

cat $* | \
python3 split.py split/ 0.1 0.1 0.8 2>&1 | tee split.log

cut -f 2,4,5 split/train.conll | sort | uniq -c | sed s/'^[^0-9]*\([0-9][0-9]*\)[ \t][ \t]*'/'\1\t'/g > train.dict