#!/bin/bash
# convert DDD paula data to conll
# note that this converter is specific to this data
# it relies on non-standard assumptions: 
# - the original text is preserved as a comment
# - the xpointer structure is either an anchor ("#tok_5") or a continuous span ("xpointer(id('tok_21')/range-to(id('tok_23')))")
# - only these fragments are supported, no complex xpointers
# - no discontinuous elements
# - we assume that no overlaps exist
# - we assume that all xpointers in *Seg.xml files point to tokens, not to anything else
# - we assume that all xpointers in *Seg_....xml files point to the corresponding *Seg.xml file
# - we assume that all elements are given in document order
# - base segmentation in *.tok.xml
# - segments: only <mark> elements supported
# - expect one annotation per line, followed by text as comment
# - expect fixed argument order

##########
# CONFIG #
##########

SRC=zips/paula_1-0.zip

# set to your CoNLL-Merge installation
# install from https://github.com/acoli-repo/conll-merge, make sure $MERGE is executable
CONLL_MERGE=~/conll
MERGE=$CONLL_MERGE/cmd/merge.sh

###########
# EXTRACT #
###########

if [ ! -e tmp ]; then
	mkdir tmp;
	cd tmp;
	unzip ../$SRC
	cd -
fi;

for base in `find tmp | grep '.tok.xml$' |sed s/'\.tok\.xml$'//`; do
	path=`echo $base | sed s/'.*tmp\/'//`

	##########
	# TOKENS #
	##########
	# cols: TOKEN WORD 
	# row: all tokens

	echo $path 1>&2
	tok=$base.tok.xml;
	
	( # HEADER
	echo "HEADER:TOKEN	WORD";
	echo;
	echo "# "$path;
	
	# BODY
	grep -a '<mark ' $tok | \
	perl -pe '
		s/.*id="([^"\n]+)".*<!--\s*([^\n]+)\s*-->\s*$/$1\t$2\n/g;
	' ) > $base.conll 
	
	head $base.conll 1>&2
	
	echo 1>&2

	for seg in $base*Seg.xml; do
	  if [ -e $seg ]; then

 	    ############
		# SEGMENTS #
		############
		# cols: TOKEN WORD SEG SEG_ID
			# SEG: segment id using a simplified IOBES encoding (B-, E-, S-) for segment ids [I- is added by $MERGE]
			# SEG_ID: plain segment id, as used in annotations, at the first element of the span
		# row: skipping intermediate and non-annotated tokens

		segType=`echo $seg | perl -pe 's/.*[^a-zA-Z0-9]([a-zA-Z0-9]+)Seg.xml$/$1/;'`
		( # HEADER
		echo "HEADER:TOKEN	WORD	"$segType"	"$segType"_ID";
		echo;
		
		# BODY
		grep -a '<mark ' $seg | \
		perl -e '
			while(<>) {
				if(m/.*href="#tok_.*/) {
					s/.*id="([^"\n]+)"[^>\n]+href="#(tok_[0-9]+).*<!--\s*([^\n]+)\s*-->\s*$/$2\t$3\tS-\1\t\1\n/g;
					print;
				} elsif(m/.*href="#xpointer\(id\(.tok_.*/) {
					$start=$_;
					$end=$_;
					$start=~s/.*id="([^"\n]+)"[^>\n]+href="#xpointer\(id\(.(tok_[0-9]+).*<!--\s*([^\n]+)\s*\.\.\..*-->\s*$/$2\t$3\tB-\1\t\1\n/g;
					$end=~s/.*id="([^"\n]+)"[^>\n]+href="#xpointer[^"]*(tok_[0-9]+).[\)]*".*<!--.*\.\.\.\s*([^\n]+)\s*-->\s*$/$2\t$3\tE-\1\t_\n/g;
					print $start;
					print $end;
				} else {
					print "ERROR: non-matching line";	# does not happen
					print;
				}
			}
		' ) > $seg.conll 
		
		egrep -a '[^\s]' $seg.conll | head 1>&2
		
		echo 1>&2
		
		echo base segmentation for $seg 1>&2;
		if egrep -m 1 -a '^tok_' $seg.conll >&/dev/null; then
			# file contains data
			# add empty rows for every base segment
			cut -f 1 $base.conll | \
			$MERGE -- $seg.conll 2>/dev/null | \
			sed s/'\t[?]'/'\t_'/g > $seg-mrg.conll 
			
			egrep -a '[^\s]' $seg-mrg.conll | head 1>&2
			mv $seg-mrg.conll $seg.conll
				echo alles ok >& /dev/null
		else
			echo warning: no annotations found in $seg, check whether it provides token ids in the form "tok_1" etc. 1>&2
			
			cut -f 1,2 $base.conll | sed s/'$'/'\t_'/ >> $seg.conll
		fi;

		
		echo;
		
		#######################
		# SEGMENT ANNOTATIONS #
		#######################
		# cols: SEG_ID VALUE
		segBase=`echo $seg | sed s/'\.xml$'//`;
		for anno in ${segBase}_*xml; do
			if [ -e $anno ]; then
				feat=`echo $anno | sed s/'.*Seg_\(.*\).xml$'/'\1'/`

				echo annotations from $anno 1>&2
		
				( # HEADER
				echo "HEADER:"$segType"_ID	"$segType":"$feat;
				echo;
				
				# BODY
				egrep -a '<feat.*href=' $anno | \
				perl -pe '
					s/.*<feat[^>]*href="#([^"]+)".*value="([^"]*)".*/\1\t\2/g;
				' ) > $seg.feats.conll 
				
				echo 1>&2
								
				$MERGE $seg.conll $seg.feats.conll 3 2>/dev/null | \
				sed s/'\t[?]'/'\t_'/g > $seg-mrg.conll

				egrep -a '[^\s]' $seg-mrg.conll | head 1>&2
				
				if [ `cat $seg-mrg.conll | wc -l ` -lt `cat $seg.conll | wc -l ` ]; then
					sed -i s/'^\(tok_.*\)$'/'\1\t_'/g $seg.conll;
				else 
					mv $seg-mrg.conll $seg.conll
				fi;
				rm $seg.feats.conll;
				
				echo 1>&2
				
			fi;
			
		done;
		
		#################
		# DROP AUX COLS #
		#################
		# drop SEG_ID column (redundant with SEG)
		cut -f 2,4 --complement $seg.conll > $seg.tmp
		mv $seg.tmp $seg.conll
		
		###########
		# MERGING #
		###########
	
		echo append to $base.merged.conll 1>&2;
		if [ ! -e $base.merged.conll ]; then
			cp $base.conll $base.merged.conll;
		fi;
		
		echo $MERGE $base.merged.conll $seg.conll >> merge.log
		$MERGE $base.merged.conll $seg.conll 2>>merge.log | \
		sed s/'\t[?]'/'\t_'/g > $base.merged.tmp.conll;
		egrep -a '[^\s]' $base.merged.tmp.conll | head 1>&2;
		
		egrep -a -B 1 '[^\s]' $base.merged.tmp.conll | egrep -a -v '^\-\-' > $base.merged.conll.tmp;
		mv $base.merged.conll.tmp $base.merged.conll
		rm $seg.conll;
		
		echo >> merge.log
		
		echo 1>&2;
		
	  fi;
	  
		

	  
	done;
	
	sed -i -e s/'^\([^#]\)'/'# \1'/g -e s/'^# \(tok_\([0-9][0-9]*\)*\)'/'\2\t\1'/ $base.merged.conll
	
done;