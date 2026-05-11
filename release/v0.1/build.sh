#!/bin/bash
# run without arguments in the local directory

MYHOME=`dirname $0`
SRC=$MYHOME/../../src

# Heliand-BT: 
# - keep HeliPaD WORDs
# - drop provenance information originally maintained in MISC column
# - keep concatenated HeliPaD and DDD XPOS annotation, keep DDD lemmas
cat $SRC/heliand-BT/heliand-bt.conllu | sed s/'_\t[^\t]*$'/'_\t_'/g > $MYHOME/heliand-bt.conllu

# Heliand-C:
# - keep DDD WORDs
# - drop provenance information originally maintained in MISC column
# - keep HeliPaD XPOS annotation, optionally concatenated with DDD XPOS, keep HeliPaD lemmas
cat $SRC/heliand-C/heliand-c.conllu | sed s/'_\t[^\t]*$'/'_\t_'/g > $MYHOME/heliand-c.conllu

# Heliand-M:
# todo