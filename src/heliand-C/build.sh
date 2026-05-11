#!/bin/bash

MYHOME=`dirname $0`
SCRIPTS=$MYHOME/../heliand-BT/scripts

cat $MYHOME/src/helipad/heliand.conllu | \
python3 $MYHOME/drop-empty-rows.py | \
python3 $SCRIPTS/align.py 25 - $MYHOME/src/heliand-BT/heliand-bt.conllu | \
python3 $MYHOME/merge.py | \
grep -v '^#' > $MYHOME/heliand-c.conllu