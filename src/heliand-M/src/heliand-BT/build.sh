#!/bin/bash
# call without args in the local dir

MYHOME=`dirname $0`
M=$MYHOME/../txt/40001B.conll
BT_UD=$MYHOME/../../../heliand-BT/heliand-bt.conllu
SCRIPTS=$MYHOME/../../../heliand-BT/scripts/

# initial alignment with Heliand BT
if [ -s $MYHOME/heliand-bt.raw.conll ]; then
	cat $MYHOME/heliand-bt.raw.conll
else
	echo $MYHOME/heliand-bt.conll 1>&2
	# reduce cols to WORD LEMMA UPOS XPOS FEATS and skip empty words
	cat $M | grep -v '^#' | \
	#
	# align with BT_UD, drop misalignments and BT provenance column
	python3 $SCRIPTS/align.py 1000 -- $BT_UD=1 | \
	tee $MYHOME/heliand-bt.raw.conll
fi | \
\
python3 merge.py | tee heliand-bt.conllu



