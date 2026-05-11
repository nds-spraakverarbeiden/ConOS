#!/bin/bash

MRG=heliand-bt.mrg
CoNLLU=heliand-bt.mrg.conllu
OUT=heliand-bt.conllu
CONLL_RDF=~/conll-rdf
LOAD=$CONLL_RDF/run.sh' CoNLLStreamExtractor # '
WRITE=$CONLL_RDF/run.sh' CoNLLRDFFormatter'

if [ ! -s $CoNLLU ]; then
	if [ ! -s $MRG ]; then
		b4_sorted=$(
			for file in src/b4*/*/b4*conllu; do
				echo `basename $file` $file;
			done | sort | cut -f 2 -d " ")
		cat $b4_sorted | \
		python3 scripts/align.py 300 src/ddd-heliand-v1.1/ddd-heliand.parsed.conllu=1 --=1 | \
		sed s/'[\t \s]*$'// | \
		egrep '^[0-9]|^$' > $MRG;
	fi
	cat $MRG | \
	$LOAD \
		ID	WORD	LEMMA	UPOS	XPOS	FEATS	DHEAD	DEDGE	DDEPS	DMISC	\
		BID	BWORD	BLEMMA	BUPOS	BXPOS	BFEATS	BHEAD	BEDGE	BDEPS	BMISC	\
		-u scripts/merge-ddd-plus-b4.sparql | \
	$WRITE -conll ID WORD LEMMA UPOS XPOS FEATS HEAD EDGE DEPS MISC > $CoNLLU
fi;

egrep -v '^#' $CoNLLU | \
	python3 scripts/align.py 300 src/ddd-heliand-v1.1/ddd-heliand.parsed.conllu=1 --=1 | \
	sed s/'^\t.*'//g | \
	egrep '^[0-9]|^$' | \
	python3 scripts/select-annotations.py \
		-in	\
			ID WORD LEMMA UPOS XPOS FEATS HEAD EDGE DEPS MISC	\
			MID MWORD MLEMMA MUPOS MXPOS MFEATS MHEAD MEDGE MDEPS MMISC \
		-out \
			ID \
			WORD \
			LEMMA \
			UPOS \
			XPOS \
			FEATS \
			"(ID==MID?MHEAD:HEAD)" \
			"(ID==MID?MEDGE:EDGE)" \
			DEPS \
			"(ID==MID?MMISC:'DDD(r)')" | tee $OUT

	# $WRITE $*
	# the following can mix up B4 and DDD within the same sentence, thus ruining IDs
	# python3 scripts/select-annotations.py \
		# -in	\
			# DID	DWORD	DLEMMA	DUPOS	DXPOS	DFEATS	DHEAD	DEDGE	DDEPS	DMISC	\
			# BID	BWORD	BLEMMA	BUPOS	BXPOS	BFEATS	BHEAD	BEDGE	BDEPS	BMISC	\
		# -out \
			# "(BLEMMA==DLEMMA?BID:DID)" \
			# DWORD \
			# DLEMMA \
			# DUPOS \
			# DXPOS \
			# "(BLEMMA==DLEMMA?BFEATS:DFEATS)" \
			# "(BLEMMA==DLEMMA?BHEAD:DHEAD)" \
			# "(BLEMMA==DLEMMA?BEDGE:DEDGE)" \
			# "(BLEMMA==DLEMMA?BDEPS:DDEPS)" \
			# "(BLEMMA==DLEMMA?concat(BMISC,';B4'):concat(DMISC,';DDD'))" 