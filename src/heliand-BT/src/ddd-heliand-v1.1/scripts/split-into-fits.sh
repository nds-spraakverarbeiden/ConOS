#!/bin/bash
# split DDD CoNLL file into fits (sections), using the last column

file=$1
dir=$2

if [ ! -s $file ]; then
	echo file $file not found 1>&2
	echo 1>&2
	file=""
fi

if [ -z $file ]; then
	echo synopsis: $0 file.conll dir 1>&2
	echo '  file.conll DDD-CoNLL file, should have Fit id in the last columns (e.g., Hel_01.eaf)' 1>&2
	echo '  dir        target directory' 1>&2
	echo 'read file.conll and split according to values of the last column, write splits into dir' 1>&2
else
	echo 'running '$0 $file $dir 1>&2

	if [ ! -e $dir ]; then
		mkdir -p $dir
	fi;

	fits=`egrep -v '\t' $file | grep -v '#' | egrep '.' | sed s/'^.*\t'// | sort -u`
	echo fits':' $fits 1>&2
	
	for fit in $fits; do
		tgt=$dir/`basename $file | sed s/'\.conll[^\.]*$'//`.$fit.conll
		echo $file '>' $tgt 1>&2
		egrep -v '#' $file | \
		grep -B 1 $fit'$' | \
		egrep -v '^\-\-' > $tgt
	done
fi;