#!/bin/bash
# infer syntax (phrasal and dependencies) from "plain" DDD conll

#############
# CONFIGURE #
#############
# set to your CoNLL-RDF installation or get it from https://github.com/acoli-repo/conll-rdf
CONLL_RDF=~/conll-rdf

########
# INIT #
########
LOAD=$CONLL_RDF/run.sh" CoNLLStreamExtractor "
LOAD_B=$CONLL_RDF/run.sh" CoNLLBrackets2RDF "
TRANSFORM=$CONLL_RDF/run.sh" CoNLLRDFUpdater "
WRITE=$CONLL_RDF/run.sh" CoNLLRDFFormatter "

#############
# TRANSFORM #
#############
cat $* | \
sed s/'^.*\$\..*$'/'&\n'/g | \
$LOAD http://replace.me/ \
	ORIGINAL WORD LEMMA IGNORE GERMAN CLAUSE CHAPTER VERSE NORM POS_LEMMA POS INFLECTION_LEMMA INFLECTION FEATS IGNORE | \
$TRANSFORM -custom -updates \
	ddd2parse.sparql \
| \
# $WRITE -grammar
$WRITE -debug
	# $WRITE -conll ID WORD POS LEMMA HEAD EDGE