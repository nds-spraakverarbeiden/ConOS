# restore original FORM column from HeliPaD-mapped (and parsed) CoNLL-U

##########
# CONFIG #
##########

# conll merge, get it from https://github.com/acoli-repo/conll-merge
# MERGE=~/conll/cmd/merge.sh

#########
# INPUT #
#########

# UD version of HeliPaD
HELI_UD=../helipad/heliand.pruned.conllu

# UD version of DDD Heliand, automatically mapped to HeliPaD annotation and orthography, not parsed
# contains an additional comment column that provides the original form
DDD_EMU=ddd-heliand-v1.1-helipad-emulation.conll

# automatically parsed version of DDD_EMU
DDD_EMU_UD=osx_ddd-heliand.pruned.parsed.conllu

# original DDD Heliand CoNLL edition (lemma taken from there)
DDD_CoNLL=ddd-heliand-v1.1.conll

########
# PROC #
########

# align automated UD parse with HeliPaD
python3 -u align.py 100 $DDD_EMU_UD=1 $HELI_UD=1 | \
tee ddd-heliand.parsed.align-1.conll | \
#
# omit words that have not been properly aligned
grep -v '^\?' | \
#
# keep only ID. XPOS, HEAD and DEP columns of HeliPaD
cut -f 1-10,11,15,17-18 | \
#
# align automated UD parse with un-parsed version of DDD Heliand
python3 -u align.py 300 --=1 $DDD_EMU=1 | \
tee ddd-heliand.parsed.align-2.conll | \
#
# restore the original form
cut -f 1-14,25 | \
sed s/'\t#\s*'/'\t'/g | \
perl -e '
	while(<>) {
		s/\t\n/\t_\n/g; 
		s/ *;[^\t]*\n/\n/g; 
		my @forms=(split /[\t\n]/,$_)[0,14];
		#print join("\t",@forms);
		if ($forms[1] eq "_") {
			print(join("\t",(split/\t/,$_)[0..13])."\n");
		} else {
			print(join("\t", @forms)."\t".join("\t",(split/\t/,$_)[2..13])."\n");
		}
	}
' |\
tee ddd-heliand.parsed.align-3.conll | \
#
# align with original DDD CoNLL to restore lemmatization
python3 -u align.py 300 --=1 $DDD_CoNLL=0 | \
cut -f 1-14,17,25,28 | \
tee ddd-heliand.parsed.align-4.conll | \
perl -pe 's/^[\s\?\.]*\n/\n/g;' | \
\
# output
#	1	ID		9
#	2	FORM	(= DDD)	gespôn
#	3	HLEMMA	(~HeliPaD)	spanan
#	4	UPOS	(~HeliPaD)	VERB
#	5	XPOS	(~HeliPaD)	VBDI^3^SG
#	6	FEATS	_	_
#	7	HEAD	predicted HeliPaD HEAD	2
#	8	EDGE	predicted HeliPaD DEP	acl
#	9	DEPS	_	_
#	10	MISC	DDD clause status	CF_I_Rel
#	11	HID	projected HeliPaD ID	7
#	12	HPOS	projected HeliPaD XPOS	GE+VBDI^SG^3
#	13	HHEAD	projected HeliPaD head, refers to HID	1
#	14	HEDGE	projected HeliPaD DEP	acl
#	15	LEMMA	DDD Lemma	gispanan
#	16	DPOS	DDD XPOS	VVFIN
#	17	DFEATS	DDD FEATS	IND_PAST_SG_3
\
# TODO: resort to HeliPaD *projections* rather than automated annotations whereever possible (i.e., not leading to a circle etc.)
tee ddd-heliand.parsed.full.conll | \
\
# format as CoNLL-U
perl -e '
	while(<>) {
		my @forms=(split/[\t\n]/,$_);
		my $xpos=join(".", @forms[15,16]);
		$xpos=~s/\.\*$//g;
		print(join("\t", @forms[0,1])."\t".@forms[14]."\t".@forms[3]."\t".$xpos."\t".join("\t", @forms[5,6,7,8,9])."\n");
	}
' | \
tee ddd-heliand.parsed.conllu




