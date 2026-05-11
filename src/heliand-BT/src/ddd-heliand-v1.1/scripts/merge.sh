#!/bin/bash
# merge ddd*conll with HeliPaD CoNLLU representation
# call without parameters, configure via variables

##########
# CONFIG #
##########

# set to your CoNLL-Merge installation (get it from https://github.com/acoli-repo/conll-merge)
CONLL_MERGE=~/conll

# set to the source CoNLL file
DDD=ddd-heliand-v1.1.conll
HELIPAD=../helipad/heliand.conllu

########
# INIT #
########

MERGE=$CONLL_MERGE/cmd/merge.sh

HELIPAD_NORM=heliand.conllu.norm
DDD_MERGED=ddd-plus-helipad.conll

########
# PREP #
########

# prefix HELIPAD CoNLL-U with a lowercase normalized text column
# merging will be done via this column
sed -e s/'^[0-9][0-9]*\t\([^\t]*\)\t.*'/'\1\t&'/ \
	-e s/'^[^\t*<][^\t]*\t'/'\L&'/ \
	-e s/'ƀ\(\s\)'/'f\1'/g \
	-e s/'ƀ'/'b'/g \
	-e s/'\(.\)th'/'\1d'/g \
	-e s/'đ'/'d'/g \
	-e s/'\([^uh]\)uo'/'\1o'/g \
	-e s/'^hu\([aeio]\)'/'huu\1'/ \
	$HELIPAD > $HELIPAD_NORM
	
#########
# MERGE #
#########
	
# merge, note that we omit the normalized column we just created
$MERGE $DDD $HELIPAD_NORM 8 0 > $DDD_MERGED