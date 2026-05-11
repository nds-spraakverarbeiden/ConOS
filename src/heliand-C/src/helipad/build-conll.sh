#!/bin/bash
# convert heliand.psd to heliand.conll

SRC=http://www.chlg.ac.uk/helipad/heliand.psd

############
# RETRIEVE #
############

PSD=`echo $SRC | sed s/'.*\/'//g`;
if [ ! -e $PSD ]; then
	echo retrieve $SRC 1>&2;
	wget $SRC -O $PSD
fi;

###########
# CONVERT #
###########
# columns: WORD POS LEMMA PARSE
# code elements are represented as WORD with POS=CODE
# ID transformed to sentence comment (metadata)

CONLL=`echo $PSD | sed s/'\.psd$'//`.conll;

if [ -e $CONLL ]; then
	echo keep existing file $CONLL 1>&2;
else

(	echo '# WORD	POS	LEMMA	PARSE'

	cat $PSD | \
	# one sentence per line
	perl -pe '
		s/\t/ /g;
		s/ +\(/\(/g;
		s/\) +/\)/g;
		s/\r\n/\n/g;
		s/([^\s][\s^\n]*)\n/$1 /g;
	' | \
	# extract id and convert to one word per line
	perl -pe '
		s/^([^\n]+) *\(ID ([^\)]+) *\) */\n# $2\n$1/g;
		s/\) *\(/\)\n\(/g;
	' | \
	# column structure
	perl -pe '

		# FIX $
		# Where words have been broken up to facilitate parsing, the site of the break is marked with a dollar sign ($). 
		# This will break the Perl code and must be eliminated or escaped.
		s/\$-/-/g; 
		s/ \$/ /g;
		
		# FIX singleton errors
		s/\(uuord-word N\^A\^SG\)/\(N\^A\^SG uuord-word\)/g;	# fix order: (POS WORD-LEMMA)
		s/\((BEPI\^3\^SG is)\)/\($1-_\)/g;						# replace missing LEMMA by _
		s/\((ADJ\^N\^SG ser)\)/\($1-_\)/g;						# replace missing LEMMA by _
		
		# RESTRUCTURING
		if(m/^[^\n]*\(CODE.*/) {			# CODE
			s/^([^\n]*) *\(CODE +([^\)]+)\)([^\n]*)$/$2\tCODE\t_\t$1 *$3\tRULE 1/g;
		} elsif(m/^[^\n]*\*[^\n]*\).*/) {	# empty element, e.g. *exp*
			s/^([^\n]* )([^ \(\n]*\*[^\)\n ]*)([^\n]*)\n/$2\t_\t_\t$1 *$3\tRULE 2\n/g;
		} elsif(m/^[^\n]*[0-9] *\).*/) {	# index, e.g. 0
			s/^([^\n]* )([^ \(\n]*[0-9]) *(\)[^\n]*)\n/$2\t_\t_\t$1 *$3\tRULE 3\n/g;
		} elsif(m/^[^\n]*\-[^\n\) ]+ *\).*/) { # word with lemma, e.g., uuisean-wisian
			s/^([^\n]*) *\(([^ \(\)\n]+) +([^ -\(\)\n]+)-([^ -\(\)\n]+) *\)([^\n]*)\n/$3\t$2\t$4\t$1 *$5\tRULE 4\n/g;
		}
		
		# REPAIR rules for punctuations
		if(m/^[^\t]*\(.*/) {
			s/^([^\n]*) *\((["'"'"']) \2-\2 *\)([^\n]*)$/$2\t$2\t$2\t$1 \*$3\tRULE 5/g;	# fix treatment of single quotes
			s/^([^\n]*) *\((\.) ([!])-\3 *\)([^\n]*)$/$3\t$2\t$3\t$1 \*$4\tRULE 6/g;	# fix treatment of !
		}
		
		# REMOVE RULE marker (uncomment for debugging)
		s/\tRULE [0-9]+$//;
	'
	) > $CONLL
fi;