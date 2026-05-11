#!/bin/bash
# call without args in the local dir

MYHOME=`dirname $0`
HELIPAD_UD=$MYHOME/../helipad/heliand.conllu
BT_UD=$MYHOME/../../../heliand-BT/heliand-bt.conllu
SCRIPTS=$MYHOME/../../../heliand-BT/scripts/

if [ -s $MYHOME/heliand-bt.conll ]; then
	echo $MYHOME/heliand-bt.conll found, keeping it 1>&2
else
	echo $MYHOME/heliand-bt.conll 1>&2
	# reduce cols to WORD LEMMA UPOS XPOS FEATS and skip empty words
	cat $HELIPAD_UD | egrep '^([0-9].*)?$' | \
	cut -f 2-6 | \
	egrep -v '^[<\*0]' | \
	#
	# align with BT_UD, drop misalignments and BT provenance column
	python3 $SCRIPTS/align.py 300 -- $BT_UD=1 | \
	grep -v '^*' | \
	cut -f 1-5,6-14 > $MYHOME/heliand-bt.conll
fi;

echo $MYHOME/heliand-bt.conllu 1>&2
cat $MYHOME/heliand-bt.conll | python3 $MYHOME/merge.py > $MYHOME/heliand-bt.conllu


