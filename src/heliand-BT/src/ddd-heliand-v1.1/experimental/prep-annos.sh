#!/bin/bash
# converts DDD-style conll annotations from stdin or argument files

CONLLRDF=~/conll-rdf

LOAD=$CONLLRDF/run.sh" CoNLLStreamExtractor"
TRANSFORM=$CONLLRDF/run.sh" CoNLLRDFUpdater"
WRITE=$CONLLRDF/run.sh" CoNLLRDFFormatter"

cat $* | \
cut -f -14 | \
egrep -v '^\*|^\s*$|^\s*#' | #[a-zA-Z0-9].*\s' | \
egrep '[A-Z$]' | \
sed s/'\(\$\..*\)$'/'\1\n'/g | \
$LOAD http://ignore.me/ \
	WORD 	IGNORE 	LEMMA 	IGNORE 	IGNORE 		CLAUSE	CHAP	VERSE 	IGNORE 	IGNORE 	POS IGNORE 					IGNORE			FEATS 		IGNORE | \
	# text  edition lemma   rhyme   translation clause  chapter verse   comp   posLemma	pos	inflectionClassLemma    inflectionClass inflection  Hel_01.eaf
$TRANSFORM -threads 6 -custom -updates ddd2parse.sparql | \
$WRITE -grammar 
#cat; echo | \

