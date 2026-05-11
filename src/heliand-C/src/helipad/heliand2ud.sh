#!/bin/bash
# auxiliary script to develop conversion of heliand.conll to CoNLL-U

#############
# CONFIGURE #
#############
# set to your CoNLL-RDF installation or get it from https://github.com/acoli-repo/conll-rdf
CONLL_RDF=~/conll-rdf

########
# HELP #
########

echo synopsis: $0 "[ FILE1.conll [.. FILEn.conll ] ]" 1>&2;
echo "  FILEi.conll Heliand CoNLL TSV file from which to create a CoNLL-RDF dump" 1>&2
echo "  IF no arguments given AND file heliand.ttl does exist, use this as input" 1>&2
echo "  IF no arguments given AND file heliand.ttl does not exist, read CoNLL from stdin (and dump the CoNLL-RDF version in heliand.ttl)" 1>&2;
echo "Creates or returns a CoNLL-RDF dump of the Heliand CoNLL data, applies transformations and/or diagnostic queries" 1>&2
echo "Provide argument files to refresh the CoNLL-RDF dump, read from stdin to create custom subcorpora using Unix command-line tools" 1>&2

########
# INIT #
########
LOAD=$CONLL_RDF/run.sh" CoNLLStreamExtractor "
LOAD_B=$CONLL_RDF/run.sh" CoNLLBrackets2RDF "
TRANSFORM=$CONLL_RDF/run.sh" CoNLLRDFUpdater "
WRITE=$CONLL_RDF/run.sh" CoNLLRDFFormatter "
ARGS=$*

########
# LOAD #
########
# prep-annos.sparql: create conll:CAT, conll:ROLE and conll:FEAT properties, split into their components
# this is included here because it is time-consuming (recursive!)

if echo $* | egrep -m 1 '.' >&/dev/null; then
	echo creating CoNLL-RDF dump for $*, overwrite heliand.ttl 1>&2;
	cat $* | \
	$LOAD_B http://replace.me/ WORD POS LEMMA PARSE | \
	sed s/'^PREFIX\(.*\)$'/'@prefix\1 .'/ | \
	$TRANSFORM -custom -updates \
		prep-annos.sparql"{u}" | \
	tee heliand.ttl;
else if [ -e heliand.ttl ] ; then # only if no arguments given
	echo using existing CoNLL-RDF dump in heliand.ttl 1>&2;
	cat heliand.ttl;
else
	echo reading from stdin and store CoNLL-RDF dump in heliand.ttl 1>&2;
	cat | \
	$LOAD_B http://replace.me/ WORD POS LEMMA PARSE | \
	sed s/'^PREFIX\(.*\)$'/'@prefix\1 .'/ | \
	$TRANSFORM -custom -updates \
		prep-annos.sparql"{u}" | \
	tee heliand.ttl;
fi; fi | \
\
#############
# TRANSFORM #
#############
\
# just single-thread, because we want to be able to terminate immediately rather than waiting for all threads to resume
# drop that flag in production mode
#$TRANSFORM -threads 1 -custom -updates  \
$TRANSFORM -threads 4 -custom -updates  \
	heliand2ud.sparql | \
	# not yet operational:	remove-empty-tokens.sparql
\
###################
# OUTPUT or DEBUG #
###################
\
# $WRITE
	# OUTPUT: canonically formatted CoNLL-RDF data, use to store intermediate versions
$WRITE -conll ID WORD LEMMA UPOS POS FEATS HEAD EDGE DEPS COMMENT
	# OUTPUT: CoNLL data, define column structure as needed, use for final output (lossy!)
#$WRITE -debug
	# DEBUG: output canonically formatted CoNLL-RDF data with syntax highlighting, for debugging CoNLL-RDF content
# $WRITE -sparqltsv get-patterns.sparql
	# DEBUG/EXTRACT: apply diagnostic query from a SPARQL file, for developing CoNLL-RDF transformation rules
#$WRITE -grammar
	# DEBUG: text-based dependency syntax visualization, for debugging final (CoNLL TSV) output
	
# for debugging internal steps of the transformation, use the -graphsPut flag of $TRANSFORM