#!/bin/bash

URL=https://www.lwl.org/331-download/niw/html/40001B.html
HTML=`basename $URL`
TXT=`echo $HTML | sed s/'\.[^\.]*$'//`.txt
CONLL=`echo $HTML | sed s/'\.[^\.]*$'//`.conll

if [ ! -e $TXT ]; then
	if [ ! -e $HTML ]; then
		wget $URL
	fi

	w3m -T text/html $HTML -O utf-8 | tee $TXT
else cat $TXT
fi | \
python3 txt2conll.py > $CONLL