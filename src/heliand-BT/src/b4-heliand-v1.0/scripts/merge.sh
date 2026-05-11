#!/bin/bash
# merge B4 Heliand with UD editions of DDD Heliand and HeliPaD

CONLL_RDF=~/conll-rdf
LOAD=$CONLL_RDF/run.sh" CoNLLStreamExtractor '#' "
BRACKET_LOAD=$CONLL_RDF/run.sh" CoNLLBrackets2RDF '#' "
TRANSFORM=$CONLL_RDF/run.sh" CoNLLRDFUpdater -custom -updates "
WRITE=$CONLL_RDF/run.sh" CoNLLRDFFormatter "

for nr in 1 4 5 6; do 
	src=../conll/exmaralda.$nr.conll
	tgt=../conllu/b4-heliand.$nr.merged
	d=../conllu/ddd-heliand.$nr.full.conll
	h=../conllu/helipad.$nr.conllu
	if [ -e $tgt ]; then
		echo keeping $tgt 1>&2
	else
		cut -f 1,2 $src | egrep '^[0-9]|^$' > $tgt
		python3 align.py 100 $tgt=1 $d=1 | egrep '^[0-9]|^$|#' | cut -f 1,3- > $d.tmp 
		python3 align.py 100 $tgt=1 $h=1 | egrep '^[0-9]|^$|#' | cut -f 1,3- > $h.tmp
		python3 align.py 100 $src $h.tmp | egrep '^[0-9]|^$|#' > $tgt.tmp	
		python3 align.py 100 $tgt.tmp $d.tmp | egrep '^[0-9]|^$|#' > $tgt
		rm $d.tmp $h.tmp $tgt.tmp
	fi;
done

for merged in ../conllu/b4-heliand.*.merged; do
	tgt=`echo $merged | sed s/'\.merged$'//`.conllu
	cut -f 1,2,3,18,20,21,22,24,25,29,31,32,33,35,36 $merged | \
	#head -n 100 | \
	perl -e '
		while(<>) {
			if(m/\t\(\(/) {					# if a new parse starts
				if(m/\t1\t(.*\t)*1\t/) {	# and D and H annotations agree on a sentence break
					print "\n"
				}
			}
			#s/^([^\n]*\t\(\()/\n$1/g;
			print $_
		}
	' | \
	$BRACKET_LOAD ID	WORD	PARSE	HID	LEMMA	UPOS	HPOS	HHEAD	HEDGE	DID	DLEMMA	DUPOS	DPOS	DHEAD	DEDGE | \
	$TRANSFORM merged2conllu.sparql | \
	$WRITE -conll ID WORD LEMMA UPOS XPOS FEATS NEW_HEAD EDGE DEPS MISC > $tgt
	
	echo $merged '->' $tgt 1>&2
	# rm $merged
done

