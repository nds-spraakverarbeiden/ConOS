#!/bin/bash

# CoNLL-RDF
CONLL_RDF=~/conll-rdf/

LOAD=$CONLL_RDF/run.sh' CoNLLStreamExtractor # '
WRITE=$CONLL_RDF/run.sh' CoNLLRDFFormatter '

INPUT=ddd-heliand.parsed.full.conll
TMP=ddd-heliand.parsed.merged.ttl
TMP2=ddd-heliand.parsed.conllu.merged.conll
OUTPUT=ddd-heliand.parsed.conllu

if [ ! -e $TMP2 ]; then
	if [ -e $TMP ]; then
		cat $TMP;
	else
		cat $INPUT | \
		egrep '^[0-9]|^$' | \
		#$LOAD ID WORD LEMMA UPOS DHPOS _ HEAD EDGE _ MISC \
		$LOAD ID WORD LEMMA UPOS DHPOS _ HEAD EDGE _ MISC HID HPOS HHEAD HEDGE HLEMMA DPOS DFEATS \
		-u consolidate-parses.sparql | \
		tee $TMP
	fi | \
	# $WRITE -grammar
	$WRITE -conll ID WORD LEMMA UPOS XPOS FEATS HEAD EDGE DEPS MISC | \
	python3 fix-tsv.py > $TMP2
	# this creates some gaps, so we align again with the automated ddd parse
fi;

python3 scripts/align.py 300 $INPUT=1 $TMP2=1  | \
sed s/'^\s*$'// | \
egrep '^$|^[0-9]|^#' | \
python3 select-annotations.py \
	-in ID WORD DLEMMA DUPOS DHPOS DFEATS DHEAD DEDGE DDEPS MISC HID HPOS HHEAD HEDGE HLEMMA DPOS DFEATS MID MWORD MLEMMA MUPOS MXPOS MFEATS MHEAD MEDGE MDEPS MMISC \
	-out \
		ID \
		WORD \
		"(ID==MID?MLEMMA:DLEMMA)" \
		"(ID==MID?MUPOS:DUPOS)" \
		"(ID==MID?MXPOS:concat(HPOS,'|',DPOS))" \
		"(ID==MID?MFEATS:DFEATS)" \
		"(ID==MID?MHEAD:DHEAD)" \
		"(ID==MID?MEDGE:DEDGE)" \
		"(ID==MID?MDEPS:DDEPS)" \
		"(ID==MID?MMISC:concat(MISC,';a->P,PD'))" > $OUTPUT
